package sokoban;

import java.util.ArrayList;

public class SokobanSearcher extends AStarSearch
{

	private ManPathfinder manFinder = new ManPathfinder();
	private int runCounter = 0;
	
	@Override
	public int evaluateState(SokobanState state, SokobanState stateGoal)
	{
		int score = 0;
		for(Square jewel : state.jewels)
		{
			int minimumDistanceToGoal = Integer.MAX_VALUE;
			if(state.goals.contains(jewel))
			{
				continue;
			}
			for(Square goal : state.goals)
			{
				int distance = Math.abs(jewel.x - goal.x) + Math.abs(jewel.y - goal.y);
				if(distance < minimumDistanceToGoal)
				{
					minimumDistanceToGoal = distance;
				}
			}
			score += minimumDistanceToGoal;
		}
		return score;
	}

	@Override
	public ArrayList<SokobanState> expandFringe(SokobanState state)
	{
		Square[] jewelMoves = new Square[4];
		Square[] manMoves = new Square[4];
		ArrayList<SokobanState> fringe = new ArrayList<SokobanState>();
		
		for(Square jewel : state.jewels)
		{
			//Up
			jewelMoves[0] = new Square(jewel.x, jewel.y - 1);
			manMoves[0] = new Square(jewel.x, jewel.y + 1);
			
			//Down
			jewelMoves[1] = new Square(jewel.x, jewel.y + 1);
			manMoves[1] = new Square(jewel.x, jewel.y - 1);
			
			//Left
			jewelMoves[2] = new Square(jewel.x - 1, jewel.y);
			manMoves[2] = new Square(jewel.x + 1, jewel.y);
			
			//Right
			jewelMoves[3] = new Square(jewel.x + 1, jewel.y);
			manMoves[3] = new Square(jewel.x - 1, jewel.y);
			
			for(int i = 0; i < 4; i++)
			{
				if(!state.jewels.contains(jewelMoves[i]) && state.emptys.contains(jewelMoves[i]))
				{
					try
					{
						SokobanState manStart = (SokobanState)state.clone();						
						//manStart.jewels.set(manStart.jewels.indexOf(jewel), (Square)jewelMoves[i].clone());
						//manStart.emptys.remove(jewelMoves[i]);
						//manStart.emptys.add((Square)jewel.clone());
						
						SokobanState manGoal = (SokobanState)manStart.clone();
						manGoal.man = (Square)manMoves[i].clone();
						//manGoal.emptys.add((Square)manStart.man.clone());
						//manGoal.emptys.remove(manMoves[i]);
						
						if(manFinder.search(manStart, manGoal))
						{
							//Move the man to the correct position and add to fringe
							manGoal.man = (Square)jewel.clone();
							
							manGoal.emptys.add((Square)manStart.man.clone());
							manGoal.emptys.add((Square)manGoal.man.clone());
							manGoal.emptys.add((Square)jewel.clone());
							
							manGoal.jewels.set(manStart.jewels.indexOf(jewel), (Square)jewelMoves[i].clone());
							manGoal.emptys.remove(jewelMoves[i]);
							manGoal.parentState = state;
							fringe.add(manGoal);
						}
					}
					catch (CloneNotSupportedException e)
					{
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
			}
		}
		return fringe;
	}

	@Override
	public boolean isValid(SokobanState state)
	{
		for(Square jewel : state.jewels)
		{
			if(state.goals.contains(jewel))
			{
				continue;
			}
			
			boolean up = state.emptys.contains(new Square(jewel.x, jewel.y - 1)) || state.man.equals(new Square(jewel.x, jewel.y - 1)) || state.jewels.contains(new Square(jewel.x, jewel.y - 1));
			boolean down = state.emptys.contains(new Square(jewel.x, jewel.y + 1)) || state.man.equals(new Square(jewel.x, jewel.y + 1)) || state.jewels.contains(new Square(jewel.x, jewel.y + 1));
			boolean left = state.emptys.contains(new Square(jewel.x - 1, jewel.y)) || state.man.equals(new Square(jewel.x - 1, jewel.y)) || state.jewels.contains(new Square(jewel.x - 1, jewel.y));
			boolean right = state.emptys.contains(new Square(jewel.x + 1, jewel.y)) || state.man.equals(new Square(jewel.x + 1, jewel.y)) || state.jewels.contains(new Square(jewel.x + 1, jewel.y));
			
			if(!((up && down) || (left && right)))
			{
				return false;
			}
		}
		return true;
	}

	@Override
	public boolean isGoalState(SokobanState state, SokobanState stateGoal)
	{
		return state.goals.containsAll(state.jewels);
	}

	@Override
	public void infoFunction()
	{
		runCounter += 1;
		if(runCounter % 1000 == 0)
		{ 
			System.out.println("Run count: " + runCounter + "\tFringe size: " + this.openList.size());
		}
		
	}

}
