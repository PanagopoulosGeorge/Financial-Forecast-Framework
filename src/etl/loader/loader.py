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
        self.parent_institution = self.__get_parent_institution(parent_institution)
        self.data = pd.read_csv(self.data_path)

    def load(self) -> bool:
        # Make a copy of the data for importing
        data_for_import = self.data.copy()

        # Fetch existing data from the database
        existing_publications = self.__get_existing_publications_df()
        existing_areas = self.__get_existing_areas()
        existing_indicators = self.__get_existing_indicators()

        # Filter data based on existing areas
        data_for_import = self.__filter_by(data_for_import, existing_areas, 'area_areaid', 'areaid')

        # Filter data based on existing indicators
        data_for_import = self.__filter_by(data_for_import, existing_indicators, 'indic_indicid', 'indicid')

        # If no data left after filtering by areas/indicators, return False
        if data_for_import.empty:
            print("No data to import after area and indicator filtering.")
            return False
        
        # Fill NaN values
        data_for_import['value_normalized'] = data_for_import['value_normalized'].apply(self.__fill_nan_numeric)
        data_for_import['date_published'] = data_for_import['date_published'].apply(self.__fill_nan_date)

        if existing_publications.empty:
            return self.bulk_insert(data_for_import)
        
        data_for_import = data_for_import.merge(
            existing_publications,
            on=['inst_instid', 'indic_indicid', 'area_areaid', 'date_from', 'date_until', 'is_forecast'],
            how='left',
            indicator=True
        )

        # Keep only rows not present in existing publications ('left_only')
        data_for_import = data_for_import[data_for_import['_merge'] == 'left_only'].drop(columns=['_merge'])

        if data_for_import.empty:
            print("No new data to import after publication filtering.")
            return False

        # At this point, you can continue to process and insert `data_for_import` into the database.
        print(f"Preparing to import {len(data_for_import)} new records.")
        return self.bulk_insert(data_for_import)




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
    
    def __filter_by(self, df: pd.DataFrame, qs: QuerySet, df_column: str, model_column) -> pd.DataFrame:
        return self.data[self.data[df_column].isin(list(qs.values_list(model_column, flat=True)))]

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
        return pd.DataFrame(qs_publications.values()).reset_index(drop=True)