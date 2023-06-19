import warnings
warnings.filterwarnings('ignore')


def extract_data(query, database='ODSDigikala'):

    from pandas import read_sql_query
    from pyodbc import connect

    try:
        conn = connect("Driver={ODBC Driver 17 for SQL Server};Server=BIWarehousing.digikala.com;Database=" + database + ";Trusted_Connection=yes;")
        result_df = read_sql_query(query, conn)
    finally:
        try: conn.close()
        except: pass
    return result_df

def load_data(query,df=None,fast_exec=True,database='DWDigikala'):

    from pyodbc import connect

    try:
        conn = connect("Driver={ODBC Driver 17 for SQL Server};Server=BIWarehousing.digikala.com;Database=" + database + ";Trusted_Connection=yes;")
        cur = conn.cursor()

        if df is None and query:
            cur.execute(query)
            conn.commit()
        elif not df.empty:
            if fast_exec:
                cur.fast_executemany = True
            cur.executemany(query, df.values.tolist())
            conn.commit()
    finally:
        try: 
            cur.close()
            conn.close()
        except: pass

class check_data():

    def _simple():

        df = None
        df.describe()
        df.info()
        df["a"].value_counts()
        df.loc[df.duplicated()]

    def missing_values(df):

        import matplotlib.pyplot as plt
        import seaborn as sns
        plt.figure(figsize=(12, 4))
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis', yticklabels=False)


class visulize_data():

    def df_summary(df):
        print(df.shape)
        print('----------------------------------------------')
        print(df.info())
        print('----------------------------------------------')
        print(df.isna().sum())
        print('----------------------------------------------')
        print(df.nunique())
        print('----------------------------------------------')
        return df.describe().apply(lambda s: s.apply('{0:.5f}'.format))

    def correlation_heatmap(df, figsize):

        import matplotlib.pyplot as plt
        from seaborn import heatmap
        from numpy import triu

        plt.figure(figsize=figsize)
        corr = df.corr()
        mask = triu(corr)
        heatmap(corr, annot=True, mask=mask, cmap='coolwarm', linewidths=.5, fmt='.2f') 

    def distplot_boxplot_boxplotXY(df, y_label: str, x_category_list=None ):

        import matplotlib.pyplot as plt
        import seaborn as sns
        if x_category_list is None:
            x_category_list = []

        for i in df.columns:
            plt.figure(figsize=(24, 6))

            plt.subplot(1, 6, 1)
            # sns.distplot(df[i])
            df[i].hist(bins=50)

            if df[i].dtypes!='datetime64[ns]':
                plt.subplot(1, 6, 2)
                sns.boxplot(df[i])

            if i != y_label:
                plt.subplot(1, 6, 3)
                # legend --> hue=df[""]           alpha=0.1
                plt.scatter(df[i], df[y_label])

            if i in x_category_list:
                plt.subplot(1, 6, 4)
                sns.boxplot(x=df[i], y=df[y_label], palette='Wistia')

                plt.subplot(1, 6, 5)
                sns.violinplot(x=df[i], y=df[y_label], palette='Wistia')

            plt.show()

            if i in x_category_list:
                print(df[i].value_counts())

    def qq_plot(df, label):

        import pylab
        import scipy.stats as stats
        stats.probplot(df[label], dist="norm", plot=pylab)
        pylab.show()

    def fix_skewness_visual(df, label):

        import matplotlib.pyplot as plt
        import seaborn as sns
        from numpy import log
        f = plt.figure(figsize=(20, 6))

        ax = f.add_subplot(141)
        sns.distplot(df[label], bins=50, color='r', ax=ax)
        ax.set_title('y')

        from scipy.special import boxcox1p
        from scipy.stats import boxcox_normmax
        r = boxcox1p(df[label], boxcox_normmax(df[label] + 1))
        ax = f.add_subplot(142)
        sns.distplot(r, bins=40, color='g', ax=ax)
        ax.set_xscale('log')
        ax.set_title('boxcox1p')

        from scipy.stats import boxcox
        y_bc, lam, ci = boxcox(df[label], alpha=0.05)
        ax = f.add_subplot(143)
        sns.distplot(y_bc, bins=40, color='y', ax=ax)
        ax.set_xscale('log')
        ax.set_title('boxcox')

        ll = log(df[label])
        ax = f.add_subplot(144)
        sns.distplot(ll, bins=40, color='b', ax=ax)
        ax.set_xscale('log')
        ax.set_title('log')

    def plot_dist(dfs, c_cols=None, d_cols=None, hue=None, n_cols_out=4):

        import math
        import matplotlib.pyplot as plt
        import seaborn as sns

        if len(dfs) > 1: hue=None
        len_c_cols = 0 if c_cols is None else len(c_cols)
        len_d_cols = 0 if d_cols is None else len(d_cols)
        n_rows = math.ceil((len_c_cols+len_d_cols)/n_cols_out)
        fig, ax = plt.subplots(n_rows, n_cols_out, figsize=(20, n_rows*3))
        ax = ax.flatten()

        if c_cols is not None:
            for i, column in enumerate(c_cols):
                for d in dfs.keys():
                    sns.kdeplot(dfs[d], x=column, hue=hue, ax=ax[i], fill=True, label=d)
        if d_cols is not None:
            for i, column in enumerate(d_cols):
                for d in dfs.keys():
                    sns.histplot(dfs[d], x=column, hue=hue, ax=ax[i+len_c_cols], discrete=True, label=d)

        if len(dfs) > 1:
            handles, labels = ax[0].get_legend_handles_labels()
            fig.legend(list(set(handles)), list(set(labels)), loc='upper center', bbox_to_anchor=(0.5, 1), fontsize=15, ncol=3)
        plt.tight_layout()
        plt.plot()
        plt.show()

    def plot_box(df, cols, n_cols_out=4):

        import math
        import matplotlib.pyplot as plt
        import seaborn as sns

        n_rows = math.ceil(len(cols)/n_cols_out)
        fig, ax = plt.subplots(n_rows, n_cols_out, figsize=(20, n_rows*3))
        ax = ax.flatten()

        for i, column in enumerate(cols):
            sns.boxplot(df, x=column, ax=ax[i])
      
        plt.tight_layout()
        plt.plot()
        plt.show()


class preprocessing_code():

    class feature_selection():

        def k_best(x, y, k: str = 'all', score_func: str = 'f_regression',is_print:bool=0,df=None):
            from sklearn.feature_selection import SelectKBest
            from sklearn.feature_selection import f_regression, mutual_info_regression

            fs = SelectKBest(score_func=f_regression if score_func !=
                             'mutual_info_regression' else f_regression, k=k)
            fs.fit(x, y)
            x_fs = fs.transform(x)

            if is_print:
                print(df.columns)
                for i in range(len(fs.scores_)):
                    print('Feature %d: %f' % (i, fs.scores_[i]))
                import matplotlib.pyplot as plt
                plt.bar([i for i in range(len(fs.scores_))], fs.scores_)
                plt.show()

            return x_fs, fs

        def rfe_way(model,x,y):

            import matplotlib.pyplot as plt
            import pandas as pd
            #from sklearn.linear_model import LinearRegression
            from sklearn.feature_selection import RFE
            from sklearn.model_selection import GridSearchCV
            from sklearn.model_selection import KFold

            folds = KFold(n_splits = 5, shuffle = True, random_state = 100)
            model.fit(x, y)
            hyper_params = [{'n_features_to_select': list(range(1, x.shape[1]))}]
            rfe = RFE(model)  

            model_cv = GridSearchCV(estimator = rfe, 
                                    param_grid = hyper_params, 
                                    scoring= 'r2', 
                                    cv = folds, 
                                    verbose = 1,
                                    return_train_score=True)      
            model_cv.fit(x, y)
            cv_results = pd.DataFrame(model_cv.cv_results_)

            plt.figure(figsize=(16,6))
            plt.plot(cv_results["param_n_features_to_select"], cv_results["mean_test_score"])
            plt.plot(cv_results["param_n_features_to_select"], cv_results["mean_train_score"])
            plt.xlabel('number of features')
            plt.ylabel('r-squared')
            plt.title("Optimal Number of Features")
            plt.legend(['test score', 'train score'], loc='upper left')

    class fill_blanks():

        def _simple(df):

            df.dropna(subset=["column_1"])

            median = df["column_1"].median()
            df["column_1"].fillna(median, inplace=True)

        def simple_imputer(df, strategy: str = 'mean'):

            import pandas as pd
            from sklearn.impute import SimpleImputer
            # strategy --> mean median most_frequent constant
            imputer = SimpleImputer(strategy=strategy)
            imputer.fit(df)
            # imputer.statistics_
            return pd.DataFrame(imputer.transform(df), columns=df.columns)

        def KNN_imputer(df):
            from sklearn.impute import KNNImputer
            imputer = KNNImputer(n_neighbors=2, weights="uniform")
            return imputer.fit_transform(df)

    class encoding():

        def _ordinal_encoder(df):

            from sklearn.preprocessing import OrdinalEncoder
            ordinal_encoder = OrdinalEncoder()
            df_encoded = ordinal_encoder.fit_transform(df)
            ordinal_encoder.categories_

        def _one_hot_encoder(df):

            from sklearn.preprocessing import OneHotEncoder
            cat_encoder = OneHotEncoder()
            df_1hot = cat_encoder.fit_transform(df)

    class fixing_skewness():

        def boxcox1p_way(df, alpha: float = 0.5):

            from scipy.stats import skew
            from scipy.special import boxcox1p
            from scipy.stats import boxcox_normmax

            numeric_feats = df.dtypes[df.dtypes != "object"].index
            skewed_feats = df[numeric_feats].apply(
                lambda x: skew(x)).sort_values(ascending=False)
            high_skew = skewed_feats[abs(skewed_feats) > alpha]
            skewed_features = high_skew.index
            for feat in skewed_features:
                df[feat] = boxcox1p(df[feat], boxcox_normmax(df[feat] + 1))

        def boxcox_way(df, label: str, alpha: float = 0.05):

            from scipy.stats import boxcox
            y_bc, lam, ci = boxcox(df[label], alpha=alpha)
            return y_bc, lam, ci

        def log_way(df, label: str):

            from numpy import log
            return log(df[label])

    def _standard(x_train, x_test):

        from sklearn import preprocessing
        scaler = preprocessing.StandardScaler().fit(x_train)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)

    def _train_test_split(x, y):

        from sklearn.model_selection import train_test_split
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.3)
    
    class outlier():

        def find_outliers_IQR(df):

            q1 = df.quantile(0.25)
            q3 = df.quantile(0.75)
            IQR = q3-q1
            return df[((df<(q1-1.5*IQR)) | (df>(q3+1.5*IQR)))]

        def remove_outliers_IQR(df, cols:list):
    
            Q1 = df[cols].quantile(0.25)
            Q3 = df[cols].quantile(0.75)
            IQR = Q3 - Q1
            return df[~((df[cols] < (Q1 - 1.5 * IQR)) | (df[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
        
        def fill_blank_outliers_IQR(df, col):
    
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            iqr_count = df.loc[((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))),col].shape[0]
            df.loc[((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))),col] = None
            print(col,' effect : ',iqr_count)

    class undersampling():

        def RandomUnderSampler(df, target_label, random_state=None):

            from imblearn.under_sampling import RandomUnderSampler
            x_res, y_res = RandomUnderSampler(random_state=random_state).fit_resample(df.drop([target_label], axis = 1), df[target_label])
            under_sample_df = x_res
            under_sample_df[target_label] = y_res
            return under_sample_df
        
class models():

    def _pickle_model(model):
        from sklearn.externals import joblib
        joblib.dump(model, "./my_model.pkl")
        # and later...
        my_model_loaded = joblib.load("./my_model.pkl")


class model_evaluation_code():

    def _error(y_test_actual, y_test_pred):

        from sklearn.metrics import mean_squared_error, mean_absolute_error

        # MSE
        print('Mean Squared Error :', mean_squared_error(
            y_test_actual, y_test_pred))

        # MAE
        print('Mean Absolute Error :', mean_absolute_error(
            y_test_actual, y_test_pred))

    def _cross_validation(model, x, y):

        from sklearn.model_selection import cross_val_score
        from numpy import sqrt
        scores = cross_val_score(
            model, x, y, scoring="neg_mean_squared_error", cv=10)
        model_rmse_scores = sqrt(-scores)

    def _grid_search_CV(model, x, y):

        from sklearn.model_selection import GridSearchCV
        param_grid = [
            {'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]},
            {'bootstrap': [False], 'n_estimators': [
                3, 10], 'max_features': [2, 3, 4]}
        ]
        grid_search = GridSearchCV(model, param_grid, cv=5,
                                   scoring='neg_mean_squared_error',
                                   return_train_score=True)
        grid_search.fit(x, y)
        grid_search.best_params_
        grid_search.best_estimator_
        cvres = grid_search.cv_result_