import pandas as pd
from institution.models import Institutions
from indicator.models import Indicators
from geography.models import Area
from publication.models import Publishes
from django.db import transaction
from django.db.models import QuerySet  # Add this import
class DataLoader:

    def __init__(self, data_path, parent_institution):
        self.data_path = data_path
        self.parent_institution = self.__get_parent_institution(parent_institution).instid
        self.data = pd.read_csv(self.data_path)

    def load(self) -> bool:
        """
        This method is the main entry point for the DataLoader class. It will load the data from the CSV file and insert it into the database.
        """
        print("#############################################################################################################")
        print(f"Initialize loading process for institution {self.parent_institution}.")
        print("Initial data shape: ", self.data.shape)
        # drop rows with missing values in the following columns
        self.data = self.data.dropna(subset=['inst_instid', 'indic_indicid', 'area_areaid', 'date_from', 'date_until', 'value', 'is_forecast'])
        print("Data shape after dropping rows with missing values: ", self.data.shape)
        # INDICATORS
        existing_indicators_for_institution = self.__get_existing_indicators()
        filtered_data = self.__filter_by(self.data, existing_indicators_for_institution, 'indic_indicid', 'indicid')
        if len(filtered_data) == 0:
            print("No data to insert for institution {self.parent_institution}. Exiting.")
            return False
        print("Data shape after filtering by existing indicators: ", filtered_data.shape)
        # AREAS
        existing_areas = self.__get_existing_areas()
        filtered_data = self.__filter_by(filtered_data, existing_areas, 'area_areaid', 'areaid')
        if len(filtered_data) == 0:
            print("No data to insert for institution {self.parent_institution}. Exiting.")
            return False
        print("Data shape after filtering by existing areas: ", filtered_data.shape)
        # PUBLICATIONS 
        existing_publications_df = self.__get_existing_publications_df()
        existing_publications_df['date_from'] = pd.to_datetime(existing_publications_df['date_from'])
        existing_publications_df['date_until'] = pd.to_datetime(existing_publications_df['date_until'])
        filtered_data['date_from'] = pd.to_datetime(filtered_data['date_from'])
        filtered_data['date_until'] = pd.to_datetime(filtered_data['date_until'])
        print("Merging old and new publications.")
        df_merged = filtered_data.merge(existing_publications_df, 
                                        on=['inst_instid', 'indic_indicid', 'area_areaid', "date_from", "date_until"], 
                                        how='left', 
                                        indicator=True)
        new_publications = df_merged[df_merged['_merge'] == 'left_only'].drop(columns='_merge').rename(
            columns={
                    'value_x': 'value',
                    'value_normalized_x': 'value_normalized',
                    'date_published_x': 'date_published',
                    'date_updated_x': 'date_updated',
                    'is_forecast_x': 'is_forecast',
                    
            })
        if len(new_publications) == 0:
            print("No new publications to insert. Exiting.")
            return False
        print("Data shape after merging old and new publications: ", new_publications.shape)
        final_df = new_publications[['inst_instid', 'indic_indicid', 'area_areaid', 'value', 'value_normalized', 'date_from', 'date_until', 'date_published', 'date_updated', 'is_forecast']]
        return self.bulk_insert(final_df)

    @transaction.atomic
    def bulk_insert(self, new_data) -> bool:
        try:
            rows = []
            for _, row in new_data.iterrows():
                inst_instance = Institutions.objects.get(instid=row['inst_instid'])
                indic_instance = Indicators.objects.get(inst_instid = self.parent_institution, indicid=row['indic_indicid'])
                try:
                    area_instance = Area.objects.get(areaid=row['area_areaid'])
                    indic_instance = Indicators.objects.get(inst_instid = self.parent_institution, indicid=row['indic_indicid'])
                except Area.DoesNotExist:
                    print(f"Area with id {row['area_areaid']} does not exist. Skipping row.")
                    continue
                except Indicators.DoesNotExist:
                    print(f"Indicator with id {row['indic_indicid']} does not exist. Skipping row.")
                    continue    

                date_from = pd.to_datetime(row['date_from']).strftime('%Y-%m-%d')
                date_until = pd.to_datetime(row['date_until']).strftime('%Y-%m-%d')
                date_published = pd.to_datetime(row.get('date_published')).strftime('%Y-%m-%d') if row.get('date_published') else None
                date_updated = pd.to_datetime(row.get('date_updated')).strftime('%Y-%m-%d') if row.get('date_updated') else None
                publish_instance = Publishes(
                    inst_instid=inst_instance,
                    indic_indicid=indic_instance,
                    area_areaid=area_instance,
                    value=row['value'],
                    value_normalized=row.get('value_normalized'),
                    date_from=date_from,
                    date_until=date_until,
                    date_published=date_published,
                    date_updated=date_updated,
                    is_forecast=row.get('is_forecast', False)
                )
                
                rows.append(publish_instance)
            
            Publishes.objects.bulk_create(rows)
            print(f"Inserted {len(rows)} new records.")
            return True
        except Exception as e:
            print(f"Error during bulk insert: {e}")
            return False

    def __fill_nan_numeric(self, value):
        if pd.isna(value):
            return 0
        return value
    
    def __fill_nan_date(self, value):
        if pd.isna(value):
            return None
        return value
    
    def __filter_by(self, df: pd.DataFrame, qs: QuerySet, df_column: str, model_column: str) -> pd.DataFrame:
        return df[df[df_column].isin(list(qs.values_list(model_column, flat=True)))]

    def __get_parent_institution(self, parent_institution) -> Institutions:
        try:
            parent_institution = Institutions.objects.get(instid=parent_institution)
            return parent_institution
        except Institutions.DoesNotExist:
            raise Institutions.DoesNotExist(f"Institution with id {parent_institution} does not exist.")

    def __get_existing_indicators(self) -> QuerySet:
        return Indicators.objects.filter(inst_instid = self.parent_institution)
    
    def __get_existing_areas(self) -> QuerySet:
        return Area.objects.all()
    
    def __get_existing_publications_df(self) -> pd.DataFrame:
        qs_publications =  Publishes.objects.filter(inst_instid=self.parent_institution,
                                                    indic_indicid__in=self.__get_existing_indicators(),
                                                    area_areaid__in=self.__get_existing_areas())
        df_publications = pd.DataFrame(qs_publications.values()).reset_index(drop=True).rename(columns={
            'inst_instid_id': 'inst_instid',
            'indic_indicid_id': 'indic_indicid',
            'area_areaid_id': 'area_areaid'
        })
        df_publications['is_forecast'] = df_publications['is_forecast'].astype('int64')
        return df_publications