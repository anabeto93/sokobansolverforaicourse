package sokoban;

import java.util.ArrayList;

public class SokobanSolver {

	/**
	 * @param args
	 */
	public static void main(String[] args) 
	{
		main1();
	}
	
	public static void main3()
	{
		MapParser mapParse = new MapParser();
		//SokobanState initial = mapParse.getInitialSokobanState("/filedisc/Workspace/Eclipse_linux_64BIT/SokobanSolverJava/rsc/map2");
        SokobanState initial = mapParse.getInitialSokobanState("./rsc/map2");
		ManPathfinder finder = new ManPathfinder();	
		try
		{
			int x = 2;
			int y = 2;
			SokobanState goal = (SokobanState)initial.clone();
			goal.emptys.add((Square)goal.man.clone());
			goal.emptys.remove(new Square(x, y));
			goal.man = new Square(x, y);
			long startTime = System.currentTimeMillis();
			for(int i = 0; i < 10000; i++)
			{
				if(finder.search(initial, goal))
					System.out.println("Hey");
			}
			long endTime = System.currentTimeMillis();
			System.out.println("Time taken: " + (endTime - startTime));
		}
		catch (CloneNotSupportedException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public static void main2()
	{
		MapParser mapParse = new MapParser();
		//SokobanState initial = mapParse.getInitialSokobanState("/filedisc/Workspace/Eclipse_linux_64BIT/SokobanSolverJava/rsc/map2");
        SokobanState initial = mapParse.getInitialSokobanState("./rsc/map2");
		ManPathfinder finder = new ManPathfinder();
		try
		{
			int x = 4;
			int y = 4;
			SokobanState goal = (SokobanState)initial.clone();
			goal.emptys.add((Square)goal.man.clone());
			goal.emptys.remove(new Square(x, y));
			goal.man = new Square(x, y);
			System.out.println(finder.search(initial, goal));
		}
		catch (CloneNotSupportedException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	public static void main1() 
	{
		MapParser mapParse = new MapParser();
		//SokobanState initial = mapParse.getInitialSokobanState("/filedisc/Workspace/Eclipse_linux_64BIT/SokobanSolverJava/rsc/map2");
        SokobanState initial = mapParse.getInitialSokobanState("./rsc/map2");
		
		try
		{
			SokobanState goal = (SokobanState)initial.clone();
			//Update the empty list
			for(Square jewel : goal.jewels)
			{
				goal.emptys.add(jewel);
			}
			goal.jewels = new ArrayList<Square>();
			for(Square g : goal.goals)
			{
				goal.jewels.add((Square)g.clone());
			}
			//goal.jewels = (ArrayList<Square>)goal.goals.clone();
			
			SokobanSearcher searcher = new SokobanSearcher();
			long timeStart = System.currentTimeMillis();
			if(searcher.search(initial, goal))
			{
				System.out.println("Solution found");
			}
			else
			{
				System.out.println("Solution NOOOOT found");
			}
			long timeEnd = System.currentTimeMillis();
			long timeTaken = (timeEnd - timeStart) / 1000;
			System.out.println("Time taken: " + timeTaken + " seconds");
			ArrayList<SokobanState> steps = searcher.constructPathToGoal();
			String solution = "";
			for(SokobanState step : steps)
			{
				solution += step.manMovesInState;
				System.out.println(step.manMovesInState);
				mapParse.printMap(step);
				System.out.println("");
			}
			System.out.println("Solution: " + solution);
			System.out.println("Steps in solution: " + solution.length());
		}
		catch (CloneNotSupportedException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}

}
