import logging

import hydra
import joblib
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from sklearn import metrics
from sklearn.model_selection import train_test_split

import wandb

log = logging.getLogger(__name__)
from sklearn.ensemble import RandomForestClassifier


@hydra.main(version_base=None, config_path='config', config_name='config')
def my_app(cfg: DictConfig ):
    print(OmegaConf.to_yaml(cfg))

    train_df = pd.read_csv(cfg.data.csv_path)

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
    preds = model.predict(X_test)

    # Оценка
    joblib.dump(model, cfg.save_path.path_to_model)


    wandb.init(project='123', config=forest_params)
    recall = metrics.recall_score(y_test,preds , average='macro')
    # Add additional configs to wandb
    wandb.config.update({"test_size" : 0.22,
                        "train_len" : len(X_train),
                        "test_len" : len(X_test)})
    wandb.log({f'recall_score': {recall}})
    wandb.sklearn.plot_learning_curve(model, X_train, y_train)
    wandb.termlog('Logged learning curve.')
    wandb.sklearn.plot_summary_metrics(model, X=X_train, y=y_train, X_test=X_test, y_test=y_test)
    wandb.termlog('Logged summary metrics.')



if __name__ == "__main__":
    my_app()
