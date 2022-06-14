from imagecluster import calc, io as icio, postproc
import glob

if __name__ == "__main__":
    # Create image database in memory. This helps to feed images to the NN model quickly.
    images = icio.read_images('images/', size=(224, 224))  # TODO: specify YOUR image directory

    # Create Keras NN model.
    model = calc.get_model()

    # Feed images through the model and extract fingerprints (feature vectors).
    # Warning: this step may run out of memory if you have a lot of images
    fingerprints = calc.fingerprints(images, model)

    # Optionally run a PCA on the fingerprints to compress the dimensions. Use a
    # cumulative explained variance ratio of 0.95.
    fingerprints = calc.pca(fingerprints, n_components=0.95)

    # Run clustering on the fingerprints. Select clusters with similarity index
    # sim=0.5. Mix 80% content distance with 20% timestamp distance (alpha=0.2).
    clusters = calc.cluster(fingerprints, sim=0.85)  # TODO: specify YOUR choice of the similarity score

    # Create dirs with links to images. Dirs represent the clusters the images
    # belong to.
    postproc.make_links(clusters, 'results')  # TODO: specify YOUR output directory

    # TODO: un-comment if you want to plot images arranged in clusters and save plot
    # fig, ax = postproc.plot_clusters(clusters, images)
    # fig.savefig('result.png', dpi=3000)
    # postproc.plt.show()
    # cnt = 0
    # for filename in glob.iglob("test/" + '**/*.png', recursive=True):
    #     cnt += 1
    #
    # print(cnt)