from gipis2tcx.training import Training

if __name__ == '__main__':
    fname = '../docs/plan2.json'
    training = Training(fname)
    print(training.convert())
