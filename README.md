# PCB

##Dependency
Python3 ,pygame
install pygame command: pip install pygame


##Running program
```
python3 t4.py
```

##Instruction
After you input the running command, you will see the GUI interface. Press q, w, e, a, s to change different components. Press each key twice to change different direction of component.

Once you decide which component you want to use, move it to the right position that can connect two dots on the PCB and press the mouse key.

And then you need to set the name of each dot in the terminal.
You will see the instruction: (Please input a name for one dot), input "a", "b" or "c" as the name of dot.

Be careful when you input the name. The program will connect two dots with the same name and if you insert all five components in the PCB, there should be five different names for ten dots. And to make sure that the result will connect all components to a circle, you need set the name for each dot properly.

You can repeat this process for each inserting component and the maximal number of components is five and each components can only be inserted once.

After you insert all components( could be two, three, four and five), go back to the GUI interface and then there are two options. Firstly, to see all the possible solutions, press m. The program will show you the optimal solution and you can press t to see another solutions. In the terminal, you will see the debugging process, like : which combination is failed and the totall time cost of the running program.Seconly, you can press n. This is the dynamic programming and this algorithm will short the running time and only give you the optimal solution. If you try m and t, you need stop the program and run it again to try n.Make sure you remember the position and name of each dot and set the same situation and press n to compare the running time(The running time will be shown in terminal).
