import logging

import hydra
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from sklearn import metrics
from sklearn.model_selection import train_test_split

log = logging.getLogger(__name__)
from sklearn.ensemble import RandomForestClassifier


@hydra.main(version_base=None, config_path='config', config_name='config')
def my_app(cfg: DictConfig ):
    print(OmegaConf.to_yaml(cfg))

    train_df = pd.read_csv('data/all_data_disease.csv')

    train_df.drop('Unnamed: 0' , axis= 1 ,  inplace = True)
    train_df.drop('Symptom_17' , axis= 1 ,  inplace = True)


    X = train_df.iloc[:,1:].values
    y = train_df['Disease'].values
    # Формируем трейн/тест
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42)

    # Обучение модели
    model = RandomForestClassifier()
    forest_params = OmegaConf.to_container(cfg['params'])
    model.set_params(**forest_params)
    model.fit(X_train, y_train)


    # Оценка
    preds = model.predict(X_test)
    recall = metrics.recall_score(y_test,preds , average='macro')
    log.info(f'recall: {recall}')

if __name__ == "__main__":
    my_app()
