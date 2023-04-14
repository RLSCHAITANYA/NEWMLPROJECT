# the purpose for doing data transformation is to perform feature engineering ,data cleaning,
# converting category features to numerical features
import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer  #handling missing values
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

#initially providing the inputs 

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function si responsible for data trnasformation
        
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )

            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)   #}
            target_feature_train_df=train_df[target_column_name]                        #}  
                                                                                        #}1)
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)     #}
            target_feature_test_df=test_df[target_column_name]                          #}

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )
                                                                                             #}
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)  #}2)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)        #}
                                                                                             
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]  #}
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]     #}3)
                                                                                           #} 
            logging.info(f"Saved preprocessing object.")

            save_object(                                                               #}
                                                                                       #}
                file_path=self.data_transformation_config.preprocessor_obj_file_path,  #}4)
                obj=preprocessing_obj                                                  #} 
                )                                                                      #}    
   
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)





# Hey, the numbered part says that :

# 1)I basically dropped target column from train data and created two datasets
# (input_feature_train_df , target_feature_train_df ) they are like train_x and train_y.
#  Similarly, we performed it on the test dataset.

# 2. After logging, i performed fit_transform on train_X and transform on test_X using the
#  preprocessing object created earlier.

# 3.  Then i used np.c_ to concatenate the transformed train and test data

# 4. Logged and saved the file.


