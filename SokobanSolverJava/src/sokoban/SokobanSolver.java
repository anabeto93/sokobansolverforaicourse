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
	
	public static void main2()
	{
		MapParser mapParse = new MapParser();
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
				System.out.println("Steps in solution: " + searcher.constructPathToGoal().size());
			}
			else
			{
				System.out.println("Solution NOOOOT found");
			}
			long timeEnd = System.currentTimeMillis();
			long timeTaken = (timeEnd - timeStart) / 1000;
			System.out.println("Time taken: " + timeTaken + " seconds");
			ArrayList<SokobanState> steps = searcher.constructPathToGoal();
			for(SokobanState step : steps)
			{
				mapParse.printMap(step);
				try
				{
					Thread.sleep(10);
				}
				catch (InterruptedException e)
				{
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
		catch (CloneNotSupportedException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}

}
