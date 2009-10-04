package sokoban;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.MemoryUsage;
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
		return score + state.manMoveLength;
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
						//Test if the man is already standing in the correct position. If so, simply move him and the jewel
						if(manMoves[i].equals(state.man))
						{
							SokobanState manGoal = (SokobanState)state.clone();
							manGoal.emptys.add((Square)jewel.clone());
							manGoal.jewels.set(state.jewels.indexOf(jewel), (Square)jewelMoves[i].clone());
							manGoal.emptys.remove(jewelMoves[i]);
							manGoal.man = (Square)jewel.clone();
							manGoal.manMoveLength = 1;
							//Update the move string
							manGoal.parentState = state;
							switch(i)
							{
							case 0:
								manGoal.moveAction = 'U';
								break;
							case 1:
								manGoal.moveAction = 'D';
								break;
							case 2:
								manGoal.moveAction = 'L';
								break;
							case 3:
								manGoal.moveAction = 'R';
								break;
							}
							fringe.add(manGoal);
						}
						else //See if the man can get to the correct position
						{							
							SokobanState manGoal = (SokobanState)state.clone();
							manGoal.man = (Square)manMoves[i].clone();
							
							if(manFinder.search(state, manGoal))
							{
								//Move the man to the correct position and add to fringe
								//manStart.parentState = state;
								SokobanState manDone = (SokobanState)manGoal.clone(); 
								manDone.man = (Square)jewel.clone();
								
								manDone.emptys.add((Square)state.man.clone());
								manDone.emptys.add((Square)manGoal.man.clone());
								manDone.emptys.add((Square)jewel.clone());
								
								manDone.jewels.set(state.jewels.indexOf(jewel), (Square)jewelMoves[i].clone());
								manDone.emptys.remove(jewelMoves[i]);
								manDone.manMoveLength = manFinder.constructPathToGoal().size() + 1;
								manDone.parentState = manGoal;
								
								//Add the last move where the goal is actually moved, Remember that we only move up to the correct position wit
								//the finder, we do the last move 'manually'
								switch(i)
								{
								case 0:
									manDone.moveAction = 'U';
									break;
								case 1:
									manDone.moveAction = 'D';
									break;
								case 2:
									manDone.moveAction = 'L';
									break;
								case 3:
									manDone.moveAction = 'R';
									break;
								}
								fringe.add(manDone);
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
			
			if(jewel.x == 1)
				return false;
			if(jewel.y == 1)
				return false;
			if(jewel.y == 5 && jewel.x > 4)
				return false;
			
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
		MemoryMXBean mem = ManagementFactory.getMemoryMXBean();
		MemoryUsage memuse;
		if(runCounter % 1000 == 0)
		{ 
			Runtime.getRuntime().gc();
			memuse = mem.getHeapMemoryUsage();
			System.out.format("Runs so far: %d \tFringe size (open list): %d \tMemory used so far: %d MB \tMemory available: %d MB%n", runCounter, this.openList.size(), memuse.getUsed()/(1024 * 1024), memuse.getMax()/(1024 * 1024));
		}
		
	}

}
