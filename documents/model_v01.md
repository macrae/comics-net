

### Dataset

Add [Dataset Distribution (Table, maybe some graphs)]

Add [Examples of Images + All meta-data]

### ML Experiments

How should we consider what machine learning task to take on first? In the pursuit of the lofty goal of training a machine learner capable of reading, writing, and drawing a comic book, there's any number of features in the cover image metadata we may consider experimenting with. For example, we have artist metadata for most images; we could design an experiment using the pencils, inks, and colors features. For most images, we also have an on-sale date; we could design an experiment for learning era (Golden, Silver, Bronze, and Modern) features, for example, some color palettes or line styles may be strongly correlated with the era the comic was created in. We also have character labels, and for more than half of our dataset, we have a list of the characters who appear on the cover.

### Two-pass Relative Sizing

I learned a neat little trick from an Agile coach named Ron Lichty, that helps me prioritize lists of software or data science development work. First-order the tasks in the relative effort, least to highest. Assign a size of 1 to the smallest task and then ask: "is the next task half-again as large as the first task?" If it is, assign it a size of 2, else 1. Continue sizing tasks pulling from the Fibonacci Sequence, always asking: "is this task half-again as large as the previous?". This is the first pass.

Add [Sized Experiments]

The second pass, value the experiments. I have no definition of value here; it's entirely my own belief. I do have some notion of dependencies, though, which influences my valuation.

Pulling from the top, a vision model for character classification is a valuable model to have, so let's try that one.

### Where's Wolverine?

In this experiment, I will attempt to train a model that, given a comic book cover, returns a list of the characters in the cover image. The machine learning task is to return a variable-length list since some covers feature only Wolverine and others the entire X-men gamut, in which we use a multi-label classifier.

### Multi-label vs Multi-class

Describe the final activation layer - softmax vs. sigmoid

Add [Architecture Diagram]

Multi-label
```
f(CoverImage) => Array[c1, c2,... cn], for some character ci
```

Multi-class
```
f(CoverImage) => cn, for some character cn
```

### Label Space Analysis

Frequency distribution of character labels. Super long-tail.

#### Label noise.

Examples of label noise.

Add [Label Noise examples]

Approach to handling encoding error (noise), and also noticed label misclassification. Uh-oh, that's not good. Examples of label misclassification and how to handle.

#### The Dataset Artifact

Applying methods to clean scraped data is so important, cannot over emphasize this, because point blank period, if you're giving your models the same bad data over-and-over, no amount of ensembling or deeper networks is going to overcome the data quality issues. A lot of the data that we scraped is crowd-sourced and have multiple accounts posting content regularly. The backend database must support some drop-down user interface for selecting certain values - based on an intuitive sense give the homogeneity of one spelling (so, low entropy) of most character encodings.

### Feature Space Analysis






## Acknowledge