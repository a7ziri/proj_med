import argparse

import joblib
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from tqdm.notebook import tqdm

import wandb


def configure_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--savepath' , type=str, required=True)
    parser.add_argument('--train_csv_path' , type = str, required=True)
    parser.add_argument('--wandb_key' , type=str, required=True)
    return parser



def train(train_csv_path:str, savepath:str ,wandb_key:str ):

    wandb.login(key=wandb_key)

    train_df = pd.read_csv(train_csv_path)

    train_df.drop('Unnamed: 0' , axis= 1 ,  inplace = True)
    train_df.drop('Symptom_17' , axis= 1 ,  inplace = True)


    X = train_df.iloc[:,1:].values
    y = train_df['Disease'].values


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.22 , random_state=42 ,shuffle=True )


    model = RandomForestClassifier(n_estimators=300 , random_state = 42 , verbose= 100)
    model.fit(X_train, y_train)
    model_params = model.get_params()
    preds = model.predict(X_test)
    joblib.dump(model, savepath)


    wandb.init(project='123', config=model_params)

    # Add additional configs to wandb
    wandb.config.update({"test_size" : 0.22,
                        "train_len" : len(X_train),
                        "test_len" : len(X_test)})
    wandb.log({'recall_score': metrics.recall_score(y_test,preds , average='macro')})
    wandb.sklearn.plot_learning_curve(model, X_train, y_train)
    wandb.termlog('Logged learning curve.')
    wandb.sklearn.plot_summary_metrics(model, X=X_train, y=y_train, X_test=X_test, y_test=y_test)
    wandb.termlog('Logged summary metrics.')


if __name__ == '__main__':
    args = configure_parser().parse_args()
    train(args.train_csv_path, args.savepath , args.wandb_key)
