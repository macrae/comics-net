# Deep Learning for Comic Books

This project applies neural networks to comic book covers and synopses to perform a
variety of machine learning tasks, for example, character classification and comic book
synopsis generation.

### Prerequisites

Python3.6.9 is required to build and run the application. The list of third-party
dependencies can be found in the `requirements.txt` and `requirements-dev.txt` files.

### Installing

Create, activate and install dependencies into a Python3.6 environment.

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
```

## Running Tests

```
python3 -m pytest comics_net/
```

## Using the Project

This project consists of two main applications: 1) webscraping and exploratory data
analysis of comic book covers and metadata, and 2) deep learning on comic book covers
and synopses to perform a variety of machine learning tasks, such as classification
and text generation.

The good news is that the webscraping of a significant number of comic book covers and
their metadata has already been performed and the datasets already published to a public
repository for your convenience.

### Datasets

A the complete curated dataset of comic book covers with metadata and annotations for
this project can be found here: [https://comics-net.s3-us-west-1.amazonaws.com/])(https://s3.console.aws.amazon.com/s3/buckets/comics-net/?region=us-west-1&tab=overview).

Within the `comics_net` module there is a `URLs` object with attributes to different
training dataset locations, for example `URLs.justic_league` will get you the location
to a Justice League curated dataset which contains characters present on any issue of
any series of the Justice League.

|Group	|# Images	|# Labels	|
|---	|---	|---	|
|Justice League	|12,445	|16	|
|Avengers	|7,186	|16	|
|Spider-Man	|6,231	|25	|
|X-Men	|5,589	|30	|
|Archies	|5,550	|23	|
|Teen Titans	|3,557	|14	|
|Fantastic Four	|2,897	|6	|
|Defenders	|2,023	|10	|
|Legion of Super-Heroes	|1,298	|23	|
|Justice Society of America	|1,291	|12	|
|Suicide Squad	|971	|8	|
|Inhumans	|548	|6	|
|Guardians of the Galaxy	|378	|5	|
|New Gods	|338	|7	|
|Lantern Corps	|805	|20	|
|Doom Patrol	|188	|10	|

### Characters

The character labels and image counts of each dataset is provided below.

#### Justice League

|Character	|# Images	|
|---	|---	|
|Batman [Bruce Wayne]	|4,939	|
|Superman [Clark Kent/ Kal-El]	|4,062	|
|Wonder Woman [Diana Prince]	|1,806	|
|Flash [Barry Allen]	|1,472	|
|Green Lantern [Hal Jordan]	|1,024	|
|Green Arrow [Oliver Queen]	|727	|
|Aquaman [Arthur Curry]	|677	|
|Hawkman [Katar Hol/ Carter Hall]	|649	|
|Catwoman [Selina Kyle]	|579	|
|Lois Lane	|533	|
|Martian Manhunter [J'onn J'onzz]	|489	|
|Joker	|452	|
|Black Canary [Dinah Laurel Lance]	|442	|
|Cyborg [Victor Stone]	|417	|
|Jimmy Olsen	|284	|
|Hawkgirl [Shayera Thal]	|209	|


#### Avengers

|Character	|# Images	|
|---	|---	|
|Iron Man [Tony Stark]	|1,844	|
|Captain America [Steve Rogers]	|1,749	|
|Thor [Thor Odinson/ Donald Blake]	|1,645	|
|Hulk [Bruce Banner]	|1,571	|
|Doctor Strange [Stephen Strange]	|770	|
|Hawkeye [Clint Barton]	|673	|
|Vision	|599	|
|Black Panther [T'Challa]	|532	|
|Wasp [Janet Van Dyne]	|506	|
|She-Hulk [Jennifer Walters]	|505	|
|Hercules	|359	|
|Wonder Man [Simon Williams]	|265	|
|Goliath [Hank Pym]	|240	|
|Ms. Marvel [Carol Danvers]	|214	|
|Bucky [James Buchanan Barnes]	|212	|
|Captain Marvel [Carol Danvers]	|201	|


#### Spider-Man

|Character	|# Images	|
|---	|---	|
|Spider-Man [Peter Parker]	|3,473	|
|Deadpool [Wade Wilson]	|712	|
|Punisher [Frank Castle]	|629	|
|Black Widow [Natasha Romanov]	|446	|
|Spider-Woman [Jessica Drew]	|276	|
|Sandman [Wes Dodds]	|234	|
|Mary Jane Watson	|212	|
|Venom [Eddie Brock]	|204	|
|Green Goblin [Norman Osborn]	|184	|
|Doctor Octopus	|179	|
|Black Cat	|171	|
|Spider-Man [Miles Morales]	|143	|
|Spider-Girl [May Parker]	|136	|
|Vulture [Adrian Toomes]	|119	|
|Hobgoblin [Roderick Kingsley]	|114	|
|Kingpin [Wilson Fisk]	|104	|
|Spider-Man 2099 [Miguel O'Hara]	|102	|
|Spider-Woman [Gwen Stacy]	|100	|
|Scarlet Spider [Ben Reilly]	|100	|
|J. Jonah Jameson	|94	|
|Electro [Max Dillon]	|92	|
|Lizard [Curt Connors]	|84	|
|Kraven [Sergei Kravinoff]	|77	|
|Aunt May Parker	|71	|
|Gwen Stacy	|69	|


#### X-Men

|Character	|# Images	|
|---	|---	|
|Wolverine [Logan/ James Howlett]	|1,875	|
|Cyclops [Scott Summers]	|907	|
|Storm [Ororo Munroe]	|755	|
|Beast [Hank McCoy]	|725	|
|Marvel Girl [Jean Grey]	|601	|
|Scarlet Witch [Wanda Maximoff]	|588	|
|Iceman [Bobby Drake]	|558	|
|Colossus [Piotr Rasputin]	|523	|
|Nightcrawler [Kurt Wagner]	|510	|
|Angel [Warren Worthington III]	|489	|
|Rogue [Anna Marie Raven]	|417	|
|Quicksilver [Pietro Maximoff]	|326	|
|Cable [Nathan Summers]	|301	|
|Magneto [Erik Lehnsherr]	|281	|
|Gambit [Remy Etienne LeBeau]	|279	|
|Kitty Pryde [Shadowcat]	|279	|
|Professor X [Charles Xavier]	|241	|
|Havok [Alex Summers]	|212	|
|Emma Frost [White Queen]	|211	|
|Psylocke [Elizabeth Braddock]	|187	|
|Bishop [Lucas Bishop]	|144	|
|Cannonball [Sam Guthrie]	|144	|
|Banshee [Theresa Rourke Cassidy]	|133	|
|Old Man Logan [James Howlett]	|132	|
|Dazzler [Alison Blaire]	|131	|
|Domino	|131	|
|Polaris [Lorna Dane]	|126	|
|Deathlok [Luther Manning]	|117	|
|Archangel [Warren Worthington III]	|116	|
|Captain Britain [Brian Braddock]	|115	|


#### Archies

|Character	|# Images	|
|---	|---	|
|Archie Andrews	|4,352	|
|Betty Cooper	|3,618	|
|Veronica Lodge	|3,373	|
|Jughead Jones	|2,387	|
|Reggie Mantle	|1,061	|
|Moose Mason	|357	|
|Miss Grundy	|299	|
|Mr. Weatherbee	|279	|
|Chuck Clayton	|229	|
|Nancy Woods	|200	|
|Ethel Muggs	|190	|
|Hot Dog	|187	|
|Dilton Doily	|158	|
|Pop Tate	|145	|
|Mr. Lodge	|144	|
|Waldo Weatherbee	|138	|
|Dilton Doiley	|133	|
|Hiram Lodge	|129	|
|Midge Klump	|121	|
|Cheryl Blossom	|99	|
|Fred Andrews	|84	|
|Coach Kleats	|66	|
|Professor Flutesnoot	|50	|


#### Teen Titans

|Character	|# Images	|
|---	|---	|
|Robin [Dick Grayson]	|1,181	|
|Superboy [Kal-El/ Clark Kent]	|916	|
|Nightwing [Dick Grayson]	|555	|
|Starfire [Koriand'r]	|357	|
|Wonder Girl [Donna Troy]	|338	|
|Raven [Rachel Roth]	|262	|
|Atom [Ray Palmer]	|250	|
|Saturn Girl [Imra Ardeen]	|239	|
|Kid Flash [Wally West]	|231	|
|Beast Boy [Gar Logan]	|206	|
|Wonder Girl [Cassie Sandsmark]	|176	|
|Changeling [Garfield Logan]	|152	|
|Red Robin [Tim Drake]	|119	|
|Speedy [Roy Harper]	|117	|


#### Fantastic Four

|Character	|# Images	|
|---	|---	|
|Human Torch [Johnny Storm]	|1,701	|
|The Thing [Ben Grimm]	|1,375	|
|Mr. Fantastic [Reed Richards]	|929	|
|Invisible Woman [Sue Storm Richards]	|869	|
|Sub-Mariner [Namor]	|795	|
|Doctor Doom [Victor von Doom]	|415	|


#### Defenders

|Character	|# Images	|
|---	|---	|
|Power Man [Luke Cage]	|444	|
|Hellcat [Patsy Walker]	|429	|
|Silver Surfer [Norrin Radd]	|396	|
|Iron Fist [Danny Rand]	|335	|
|Daredevil [Matt Murdock]	|330	|
|Moon Knight	|236	|
|Valkyrie [Barbara Norris]	|204	|
|Nighthawk [Kyle Richmond]	|163	|
|Hedy Wolfe	|155	|
|Buzz Baxter	|143	|


#### Legion of Super-Heroes

|Character	|# Images	|
|---	|---	|
|Supergirl [Kara Danvers/ Kara Zor-El]	|613	|
|Brainiac 5 [Querl Dox]	|204	|
|Cosmic Boy [Rokk Krinn]	|201	|
|Chameleon Boy [Reep Daggle]	|186	|
|Ultra Boy [Jo Nah]	|162	|
|Lightning Lad [Garth Ranzz]	|156	|
|Phantom Girl [Tinya Wazzo]	|117	|
|Sun Boy [Dirk Morgna]	|107	|
|Timber Wolf [Brin Londo]	|102	|
|Mon-El [Lar Gand]	|100	|
|Wildfire [Drake Burroughs]	|100	|
|Colossal Boy [Gim Allon]	|99	|
|Element Lad [Jan Arrah]	|97	|
|Shrinking Violet [Salu Digby]	|92	|
|Star Boy	|92	|
|Lightning Lass [Ayla Ranzz]	|81	|
|Karate Kid [Val Armorr]	|79	|
|Shadow Lass [Tasmia Mallor]	|78	|
|Dawnstar	|72	|
|Dream Girl [Nura Nal]	|57	|
|Invisible Kid [Lyle Norg]	|54	|
|Live Wire	|53	|
|Princess Projectra	|51	|


#### Justice Society of America

|Character	|# Images	|
|---	|---	|
|Flash [Jay Garrick]	|341	|
|Green Lantern [Alan Scott]	|286	|
|Power Girl [Karen Starr]	|231	|
|Huntress [Helena Bertinelli]	|193	|
|Zatanna [Zatanna Zatara]	|181	|
|Wildcat [Ted Grant]	|114	|
|The Atom [Al Pratt]	|105	|
|Doctor Mid-Nite [Charles McNider]	|96	|
|Red Tornado [John Smith]	|94	|
|Mr. Terrific [Michael Holt]	|78	|
|Star-Spangled Kid [Courtney Whitmore]	|66	|
|Sentinel	|62	|


#### Suicide Squad

|Character	|# Images	|
|---	|---	|
|Harley Quinn [Harleen Quinzel]	|355	|
|Deathstroke [Slade Wilson]	|253	|
|Poison Ivy [Pamela Isley]	|172	|
|Deadshot [Floyd Lawton]	|132	|
|Vixen [Mari McCabe]	|77	|
|Captain Boomerang [George "Digger" Harkness]	|67	|
|Black Manta	|64	|
|Bronze Tiger [Ben Turner]	|51	|


#### Inhumans

|Character	|# Images	|
|---	|---	|
|Medusa [Medusalith Amaquelin]	|276	|
|Black Bolt [Blackagar Boltagon]	|221	|
|Crystal [Crystalia Amaquelin]	|149	|
|Gorgon [Andonis Bal]	|103	|
|Karnak	|100	|
|Triton	|92	|


#### Guardians of the Galaxy

|Character	|# Images	|
|---	|---	|
|Rocket Raccoon	|180	|
|Drax the Destroyer	|147	|
|Star-Lord [Peter Quill]	|137	|
|Groot	|135	|
|Gamora	|116	|


#### New Gods

|Character	|# Images	|
|---	|---	|
|Mister Miracle [Scott Free]	|134	|
|Orion	|99	|
|Darkseid	|88	|
|Big Barda	|78	|
|Lightray	|30	|
|Oberon	|25	|
|Granny Goodness	|22	|


#### Lantern Corps

|Character	|# Images	|
|---	|---	|
|Green Lantern [Kyle Rayner]	|275	|
|Green Lantern [John Stewart]	|223	|
|Green Lantern [Guy Gardner]	|222	|
|Green Lantern [Kilowog]	|81	|
|Green Lantern [Simon Baz]	|68	|
|Red Lantern [Atrocitus]	|26	|
|Green Lantern [Jessica Cruz]	|23	|
|Green Lantern [Arisia]	|21	|
|Green Lantern [Katma Tui]	|21	|
|Red Lantern [Bleez]	|21	|
|Green Lantern [Salaak]	|20	|
|Green Lantern [Soranik Natu]	|20	|
|Green Lantern [Arisia Rrab]	|18	|
|Red Lantern [Guy Gardner]	|17	|
|Green Lantern [Isamot Kol]	|14	|
|Blue Lantern [Saint Walker/ Bro'Dee Walker]	|13	|
|Green Lantern [Vath Sarn]	|12	|
|Green Lantern [Hannu]	|11	|
|Green Lantern [Sodam Yat]	|11	|
|Red Lantern [Zilius Zox]	|10	|


#### Doom Patrol

|Character	|# Images	|
|---	|---	|
|Robotman [Cliff Steele]	|159	|
|Negative Man [Larry Trainor]	|107	|
|Elasti-Girl [Rita Farr]	|99	|
|The Chief [Niles Caulder]	|26	|
|Fever	|16	|
|Freak	|15	|
|Tempest [Joshua Clay]	|14	|
|Negative Woman [Valentina Vostok]	|13	|
|Kid Slick	|12	|
|Nudge	|12	|


## Authors

* **Sean MacRae** - *Initial work* - [macrae](https://github.com/macrae)

## License

`<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.`

## Acknowledgments

Thanks to the good folks at [comics.org](https://comics.org) for their hard work building
and maintaining one of the richest databases of graphic novel covers and metadata. I
could not have done this without you!
