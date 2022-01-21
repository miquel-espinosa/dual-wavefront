# Dual wavefront algorithm
A tree-based algorithm with two wavefronts for path-planning in an unknown discrete environment. The two fronts simultaneously exist and expand. In this version, there is no prior knowledge of the position of goal, therefore, no heuristics can be used.

## Report
For a more in-depth overview of the work carried out, check the following pdf report: [Dual Wavefront Algorithm](https://github.com/miquel-espinosa/dual-wavefront/blob/master/P3_Robots.pdf)

## Dependencies
To run this project you will need installed: `python 3`, `numpy`, `matplotlib`, `scipy`, `tkinter`, `math`, `subprocess`.

## Run the project
```
python3 main.py
```

## Demos
Some demos of the output generated are shown in the following animations (created with Matplotlib).
### Simple block scenario
A simple block scenario simulation is carried out.
![Alt Text](https://github.com/miquel-espinosa/dual-wavefront/blob/master/videos/gifs/simple.gif?raw=true) 
In this simulation, it is explicitly shown the tree as it expands. Note that optimum paths are being expanded on-the-go. Therefore, once both "waves" meet, it is only a matter of backtracking through the parent nodes back to the original root.
![Alt Text](https://github.com/miquel-espinosa/dual-wavefront/blob/master/videos/gifs/simple-tree.gif?raw=true) 
### Blocks map
A more complex layout is proposed by randomly distributing block obstacles in the search space.
![Alt Text](https://github.com/miquel-espinosa/dual-wavefront/blob/master/videos/gifs/random.gif?raw=true)
A grid of uniformly distributed blocks is input to the dual wavefront planner.
![Alt Text](https://github.com/miquel-espinosa/dual-wavefront/blob/master/videos/gifs/dots.gif?raw=true)
\
\
A plan view search space is proposed.
![Alt Text](https://github.com/miquel-espinosa/dual-wavefront/blob/master/videos/gifs/room.gif?raw=true)
### Laberynths
Laberynths are constructed to test the limits of the planner. Firstly, a simple labyrinth is constructed.
![Alt Text](https://github.com/miquel-espinosa/dual-wavefront/blob/master/videos/gifs/laberinto2.gif?raw=true)
A more challenging labyrinth follows.
![Alt Text](https://github.com/miquel-espinosa/dual-wavefront/blob/master/videos/gifs/laberinto1.gif?raw=true)
A labyrinth with multiple holes and simultaneously open tree branches.
![Alt Text](https://github.com/miquel-espinosa/dual-wavefront/blob/master/videos/gifs/holes.gif?raw=true)
A huge laberynth of 99x99 cells grid.
![Alt Text](https://github.com/miquel-espinosa/dual-wavefront/blob/master/videos/gifs/huge.gif?raw=true)


## Acknowledgments
Laberynths generation is taken from:
* [bactracking-maze-generator](https://github.com/jbarciv/Backtracking-Maze-Generator)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

<!---
## Description

An in-depth paragraph about your project and overview of use.

## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
--->
