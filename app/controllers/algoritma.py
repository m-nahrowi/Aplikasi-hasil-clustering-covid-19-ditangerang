from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from sklearn import preprocessing
from math import sqrt, floor


def algoritm():
    k  = 3 # Jumnlah K nya
    # Kalo K = 3 ikut juga 3 label data nya kalo 5 ikut 5 juga, bisa di enable atau disable pada label data di bawah ini
    label_data = [
        # ['Tidak Terdampak', '#27ae60'], # Kalo 0
        # ['Tidak Ada Kasus', '#2ecc71'],
        ['Resiko Rendah', '#f1c40f'],
        ['Resiko Sedang', '#f39c12'],
        ['Resiko Tinggi', '#e74c3c']
    ]

    df = pd.read_csv('static/data_covid_kota_tangearng.csv')
    dc = df.iloc[:, 2:6]
    # Normalisasi Data
    scaler    = preprocessing.MinMaxScaler(feature_range=(0, 4))
    names     = dc.columns
    d         = scaler.fit_transform(dc)
    scaled_df = pd.DataFrame(d, columns=names)
    print('========== DATASET NORMAL ==========')
    print(dc)
    print('========== SCLAED DATASET ==========')
    print(scaled_df)

    X_std = scaled_df.to_numpy()
    desa  = df.iloc[:, 1].to_numpy()
    # Start K-Means
    naive_centroids = naive_sharding(X_std, k)
    print(naive_centroids)
    km = KMeans(n_clusters=k, init=naive_centroids, n_init=1, max_iter=300)
    km.fit(X_std)
    hasil_label = km.labels_
    print("========== HASIL CLUSTER LABEL ==========")
    print(hasil_label)
    df['clustering'] = hasil_label.tolist()

    return label_data, df, hasil_label


# Reference : https://www.kdnuggets.com/2020/06/centroid-initialization-k-means-clustering.html
def naive_sharding(ds, k):
    """
    Create cluster centroids using deterministic naive sharding algorithm.
    
    Parameters
    ----------
    ds : numpy array
        The dataset to be used for centroid initialization.
    k : int
        The desired number of clusters for which centroids are required.
    Returns
    -------
    centroids : numpy array
        Collection of k centroids as a numpy array.
    """

    def _get_mean(sums, step):
        """Vectorizable ufunc for getting means of summed shard columns."""
        return sums/step

    n = np.shape(ds)[1]
    m = np.shape(ds)[0]
    centroids = np.zeros((k, n))

    composite = np.mat(np.sum(ds, axis=1))
    ds = np.append(composite.T, ds, axis=1)
    ds.sort(axis=0)

    step = floor(m/k)
    vfunc = np.vectorize(_get_mean)

    for j in range(k):
        if j == k-1:
            centroids[j:] = vfunc(np.sum(ds[j*step:,1:], axis=0), step)
        else:
            centroids[j:] = vfunc(np.sum(ds[j*step:(j+1)*step,1:], axis=0), step)

    return centroids
