import pandas as pd
from institution.models import Institutions
from indicator.models import Indicators
from geography.models import Area
from publication.models import Publishes
from django.db import transaction
from django.db.models import QuerySet  # Add this import
import time
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
        time.sleep(1)
        print(f"Initialize loading process for institution {self.parent_institution}.")
        time.sleep(1)
        print("Initial data shape: ", self.data.shape)
        time.sleep(1)
        # drop rows with missing values in the following columns
        self.data = self.data.dropna(subset=['inst_instid', 'indic_indicid', 'area_areaid', 'date_from', 'date_until', 'value', 'is_forecast'])
        print("Data shape after dropping rows with missing values: ", self.data.shape)
        time.sleep(1)
        # INDICATORS
        print(" =============== 1. Filtering by existing indicators ===============")
        existing_indicators_for_institution = self.__get_existing_indicators()
        filtered_data = self.__filter_by(self.data, existing_indicators_for_institution, 'indic_indicid', 'indicid')
        if len(filtered_data) == 0:
            print("No data to insert for institution {self.parent_institution}. Exiting.")
            return False
        time.sleep(1)
        print("Data shape after filtering by existing indicators: ", filtered_data.shape)
        # AREAS
        time.sleep(1)
        print(" =============== 2. Filtering by existing areas ===============")
        existing_areas = self.__get_existing_areas()
        filtered_data = self.__filter_by(filtered_data, existing_areas, 'area_areaid', 'areaid')
        if len(filtered_data) == 0:
            print("No data to insert for institution {self.parent_institution}. Exiting.")
            return False
        time.sleep(1)
        print("Data shape after filtering by existing areas: ", filtered_data.shape)        
        

        print(" =============== 4. Separate projections from historical data  =============== ")
        historical_data = filtered_data[filtered_data['is_forecast'] == 0]
        forecast_data = filtered_data[filtered_data['is_forecast'] == 1]
        time.sleep(1)
        print("Forecasts records: ", len(forecast_data))
        print("Historical records: ", len(historical_data))

        print(" =============== 5. Inserting historical data =============== ")
        if len(historical_data) > 0:
            inserted = self.bulk_insert(historical_data)
            if not inserted:
                print("Error inserting historical data. Exiting.")
                return False
        else:
            print("No historical data to insert.")
        time.sleep(1)
        print(" =============== 6. Inserting forecast data =============== ")
        if len(forecast_data) > 0:
            inserted = self.bulk_insert(forecast_data)
            if not inserted:
                print("Error inserting forecast data. Exiting.")
                return False
            return inserted
        else:
            print("No forecast data to insert.")

    @transaction.atomic
    def bulk_insert(self, new_data) -> bool:
        try:
            
            institutions_cache = {
                inst.instid: inst for inst in Institutions.objects.all()
            }
            indicators_cache = {
                (indic.inst_instid, indic.indicid): indic for indic in Indicators.objects.filter(inst_instid=self.parent_institution)
            }
            areas_cache = {
                area.areaid: area for area in Area.objects.all()
            }

            rows = []
            for _, row in new_data.iterrows():
                
                inst_instance = institutions_cache.get(row['inst_instid'])
                if not inst_instance:
                    print(f"Institution with id {row['inst_instid']} does not exist. Skipping row.")
                    continue
                
                area_instance = areas_cache.get(row['area_areaid'])
                if not area_instance:
                    print(f"Area with id {row['area_areaid']} does not exist. Skipping row.")
                    continue

                indic_instance = indicators_cache.get((inst_instance, row['indic_indicid']))
                if not indic_instance:
                    print(f"Indicator with id {row['indic_indicid']} does not exist. Skipping row.")
                    continue
                # Process date fields
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
            print("Number of records: ", len(rows))
            

            # Use bulk_create with batching for large datasets
            Publishes.objects.bulk_create(rows, batch_size=500)
            print(f"Inserted {len(rows)} new records.")
            return True

        except Exception as e:
            print(f"Error during bulk insert: {e}")
            return False
    
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