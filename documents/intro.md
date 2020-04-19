<!-- Draft an Intro article (headline < 7 words, content < 1600 words) -->

<!-- Tips: 1) short parapgraphs, 2) compelling imagery, 3) break it up with headings, 5) simple english -->

Introduction

Achievements in machine learning over the last five years, especially for vision and natural language, have been striking. In terms of efficacy, compare these best-in-class benchmarks for [some task] between 2015 and 2019. 

(Table)

The proliferation of open-source software coupled with relatively cheap, ephemeral cloud compute resources, has led to a world where achieving state of the art machine learning results is within reach of the hobbyist. 

Better living through AI is as much about automating the menial as it is about machine-augmented creativity. As machines are empowered to perform an increasing number of more human-like tasks, it becomes difficult to separate their work from our own. Humans still reign supreme in many ways, but machines hold their own heavyweight belts. Augmenting human creativity with machine learning provides a unique opportunity to explore the shared space between humans and machines.

Machine Learning as Art

When I read excerpts from a new Harry Potter book that was written by a machine [https://botnik.org/content/harry-potter.html]), I gotta laugh, because as bad as it is by my standards, for all its shortcomings and irreverence it's still somehow surprisingly good.

"The castle grounds snarled with a wave of magically magnified wind. The sky outside was a  great black ceiling, which was full of blood. The only sounds drifting from Hagrid's hut were the disdainful shrieks of his own furniture. Magic:  it was something that Harry Potter thought was very good."

Reading machine prose can feel like accessing some artifact passed through the membrane of an alternate computer-verse. At first glimpse, it feels the same, but pretty quickly, you realize everything is just a bit off. It's Bizarro's world of Earth-29 in opposition to Superman's world of Earth-0. The trope of Earth-29 is subversion, so Bizarro puts puppies in trees and burns down houses. He lives on the planet Htrae and is a member of the Unjustice League because those things are literally the opposite of Superman. From our vantage point on Earth-0, Earth-29 is more of a commentary on Superman than anything else, though. Bizarro is just there to provide enough contrast for the Man of Steel to really pop, to amplify his already saturated blue and red "S," the salt in the brownies.

"Us do opposite of all Earthly things! Us hate beauty! Us love ugliness! Is big crime to make anything perfect on Bizarro World!" - Bizarro

Not every alternate universe is as stark a comparison as Earth-29, though. Some are more nuanced and draw subtler parallels, like Eath-10, the Nazi-themed world where everybody's favorite caped crusaders formed under the third-Reich. What can a world where the Justice League fights alongside Adolf Hitler tell us about our own beliefs and morals?

On Earth-23, where every superhero is black, Superman is also the President of the United States. Wonder Woman, who is called Nubia, brought anti-war technology to the world. What can a world where the bonds of slavery don't exist, tell us about our own social construct? What can Earth-11, the matriarchal world of Superwoman, Batwoman, and Wonder Man tell us about our own sex and gender biases?

As machines get better at appearing human, these computer-verse artifacts start to feel less like something from the Bizarro-verse and more like something from a universe indistinguishable to our own. We are moving from a world where computer-generated media is interesting because of what it can tell us about us, to a world where it is interchangeable with our own. How simultaneously wondrous and horrifying. Any technology subject to the whims of its practitioner can be bent to their will. What ethical AI entails is an ongoing and important conversation, so the topic of ethics in AI will be addressed when appropriate. It's important to reflect on the implications of this technology and how it has been, or could be, weaponized.

My contribution to machine learning for the common, and creative, good is rooted in an art form I very much enjoy: comic books. The end goal is to take this all the way to the bleeding edge of machine learning. Imagine an algorithm that can interpret a comic book from cover to cover. One that understands artistic style and panel design, or can describe characters and story arc. An algorithm that can draw and write its very own comic books is a lofty goal, even by 2020 standards.

To start, I am going to treat reading, writing, and drawing as independent tasks. In practice, when reasoning about an entire comic book end to end, there are joint probabilities between these three spaces. The likelihood that I am reading an Animal Man story is conditionally based on whether I am viewing drawings containing Bernhard "Buddy" Baker, his Animal Man persona, and a slew of animals, such as dinosaurs, birds, fish, ants, spiders, snakes, dogs, and cockroaches. As I progress towards more sophisticated models that can perform multiple tasks conditioned on the outcomes of other tasks, I can leverage the learnings of these independent investigations.

An Approach

Since the goal is lofty, it's best to break it down into manageable pieces and chalk up some early wins. Small, early successes will make me feel good about how I'm spending my time, but also force me to gain a better understanding of the problem space and uncover and work through any unknowns. Fun fact: there are always unknowns, and they always take twice as long as expected.

When breaking down any machine learning task, I like to ask myself: as a human, how would I do this thing, step-by-step? 

How to Read a Comic Book
Step 1 - The Cover

As a human, how do I read a comic book? Well, I'd say I always start with the cover. 

In my experience, what I know about comic book cover art is that it is often artistically distinct from the book's interior art. Publishers hire cover artists or may feature many artists for a single issue, putting out a smattering of variant covers. Sometimes publishers will bring in heavy hitters to draw covers for launching series to boost sales. They may also have requirements for cover art based on their own belief of what sells. Have you ever seen an issue of Batman without the Dark Knight crouched on the eve of a roof or swinging effortlessly through the air?

Specifically, as a human, given a comic book cover, I can identify most of the characters on it. I can give a description of the scene shown, like who is fighting who, or does it take place in space? I can determine the series name from its title and may be able to infer part of the story through subtitles and text. I have a relative sense of the era it was published, based on the art, and I may be able to determine the artist. 

Given the description of the human task, reading a comic book cover, I need to frame the machine learning tasks that proxy an ability to reason as described above.

Identify the characters on it
Describe what or where something is happening
Identify the series and publisher
Identify the era it was published
Identify the cover artist

Multi-label
The task of identifying which characters are present on a given cover can be stated as a multi-label model.

Given some input image x, return a list of character names [c1, c2, c3, ...] for ci the ith character on the cover.

Multi-class
The task of identifying the series publisher, era, and cover artist are all multi-class models.

Given some input image x, return a value yi indicating the image to be class i from the possible list of classes [y1, y2, y3, ...]

Encoder/Decoder
The task of describing a scene taking place on a comic book cover is an encoder/decoder model.

Given some input image x, return a string of length n where the string describes the image.

It's one thing to dream up a bunch of lofty, high falutin machine learning tasks to do something as trivial as reading a comic book. It's another thing to actually do it. For starters, we need labeled data. I can't train a machine learning model to spot Archie Andrews from Jughead Jones unless I give it images and tell it: "this one has Archie, this one does not have Archie, etc."

This raises an important point, and one I feel needs to be highlighted. Give the data a voice at the product table. Just because I would like to train a model that is capable of describing what is taking place on a cover, does not mean that I actually can. My own personal skill-fit aside and whether I am capable or not is moot if the underlying data does not support the task I'd like to perform. 

So... All We Need is Some Labeled Data

This is a perfect segue into my next article about web scraping and writing a Python application to create an entirely new dataset for training a novel machine learning model.

They say that 80% of data science work is not actually modeling, but everything else required to be equipped to model. That has been and continues to be, my personal experience when working on something new and novel. Curating a dataset with enough images and labels is more hacking than it is science. Iterating through edge cases while programmatically traversing a statically generated website and parsing HTML refs to recursively slurp up variant images is a grind. Then, after dozens of hours vacuuming up as many comic book images and metadata as possible, learning you excluded a metadata field that would really help in a particular machine learning task. Web scraping, at least for me, is to proper software development as the play-doh sculpture is to a fine art. I'm sure there are folks out there who make an appropriate science of web-scraping. Still, I'm not one of them, and so what follows is basically what I learned stumbling through a darkened room and hitting every single piece of furniture on my way out.