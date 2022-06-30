# image-clustering

## Description
This tool performs unsupervised clustering of 2D images. Specifically, it generates "fingerprint" embeddings that are expressive in terms of image features by running a pre-trained ResNet model, and uses the "fingerprint" embeddings to cluster images that are alike.

Since our goal is to find and evaluate similarity of assembly design models, you may find it helpful to **use this tool to cluster assembly.png thumbnail images**, which can serve as a baseline or as a starting point.

## Installing

To use the cluster_body_images.py code, you would need to install [imagecluster](https://elcorto.github.io/imagecluster/index.html) with the following steps:

1. Clone imagecluster at this directory

```
git clone https://github.com/elcorto/imagecluster.git
```

2. Install

```
cd imagecluster
pip install -e .
```

3. Make slight modifications to the imagecluster for better compatibility

```
# in postproc.py, change function "make_links()" in "postproc.py" to the following
# for COPYING images instead of creating symbolic links

def make_links(clusters, cluster_dr):
    """In `cluster_dr`, create nested dirs with symlinks to image files
    representing `clusters`.

    Parameters
    ----------
    clusters : see :func:`~imagecluster.calc.cluster`
    cluster_dr : str
        path
    """
    print("cluster dir: {}".format(cluster_dr))
    if os.path.exists(cluster_dr):
        shutil.rmtree(cluster_dr)
    for csize, group in clusters.items():
        for iclus, cluster in enumerate(group):
            dr = pj(cluster_dr,
                    'cluster_with_{}'.format(csize),
                    'cluster_{}'.format(iclus))
            for fn in cluster:
                link = pj(dr, os.path.basename(fn))
                source = os.path.abspath(fn)
                target = link
                os.makedirs(os.path.dirname(link), exist_ok=True)
                shutil.copyfile(source, target)

#####################################################################
# if your computer cannot manage multiprocessing when reading huge amount of images
# change the function "read_images()" in "io.py" to the following:

from tqdm import tqdm

def read_images(imagedir, size, ncores=mp.cpu_count()):
    """Load images from `imagedir` and resize to `size`.

    Parameters
    ----------
    imagedir : str
    size : sequence length 2
        (width, height), used in ``Image.open(filename).resize(size)``
    ncores : int
        run that many parallel processes

    Returns
    -------
    dict
        {filename: 3d array (height, width, 3), ...}
    """

    files = get_files(imagedir)
    ret = []

    for file in tqdm(files, desc="Processing images"): # also adding progress bar for convenience
        ret.append(_image_worker(file, size=size))

    return {k: v for k, v in ret if v is not None}

```

---

## Usage
- Place the 2D images that you want to perform clustering inside the folder "images"
- Run the following commands to perform image clustering
```
python cluster_images.py
```

