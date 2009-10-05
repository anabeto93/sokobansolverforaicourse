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
		boolean optimizeForMinimumManMoves = true;

		if(optimizeForMinimumManMoves)
		{
			//
			//Optimize for minimal man moves!!!
			//
			int numberOfMovesTakenToGetToState = 0;
			SokobanState searcher = state;
			while(!searcher.equals(this.stateInitial))
			{
				numberOfMovesTakenToGetToState += searcher.manMovesInState.length();
				searcher = searcher.parentState;
			}
			//length += searcher.movesSoFar.length();
			return numberOfMovesTakenToGetToState;
		}
		else
		{	
			//
			//Optimize for minimal jewel moves
			//
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
							//Update the move string
							manGoal.parentState = state;
							switch(i)
							{
							case 0:
								manGoal.manMovesInState = "U";
								break;
							case 1:
								manGoal.manMovesInState = "D";
								break;
							case 2:
								manGoal.manMovesInState = "L";
								break;
							case 3:
								manGoal.manMovesInState = "R";
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
								manDone.manMovesInState = manFinder.getMoves();
								manDone.parentState = state;
								
								//Add the last move where the goal is actually moved, Remember that we only move up to the correct position wit
								//the finder, we do the last move 'manually'
								switch(i)
								{
								case 0:
									manDone.manMovesInState += 'U';
									break;
								case 1:
									manDone.manMovesInState += 'D';
									break;
								case 2:
									manDone.manMovesInState += 'L';
									break;
								case 3:
									manDone.manMovesInState += 'R';
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
			
			//Now check to see if the jewel is positioned along a wall in a way that makes it impossible to get it away from the wall,
			//and onto a goal!
			if(!up)
			{
				//Check if up is a hole, before reaching a wall
				boolean upEscaped = false;
				Square t;
				for(int i = 0; i < 10; i++)
				{
					//first go right
					t = new Square(jewel.x + i, jewel.y);
					if(!(state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
					{
						if(jewel.y != 1)
							System.out.println("Error Y1 in algo!" + jewel.y);
						return false;
					}
					t = new Square(jewel.x + i, jewel.y - 1);
					if((state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
					{
						upEscaped = true;
						break;
					}
				}
				if(!upEscaped)
				{
					for(int i = 0; i < 10; i++)
					{
						//Then go left
						t = new Square(jewel.x - i, jewel.y);
						if(!(state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
						{
							if(jewel.y != 1)
								System.out.println("Error Y1 in algo!" + jewel.y + "D");
							return false;
						}
						t = new Square(jewel.x - i, jewel.y - 1);
						if((state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
						{
							break;
						}
					}
				}
			}
			
			if(!down)
			{
				//Check if up is a hole, before reaching a wall
				boolean downEscaped = false;
				Square t;
				for(int i = 0; i < 10; i++)
				{
					//first go right
					t = new Square(jewel.x + i, jewel.y);
					if(!(state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
					{
						if(jewel.y != 5 || jewel.x <= 4)
							System.out.println("Error Y2 in algo! " + down);
						return false;
					}
					t = new Square(jewel.x + i, jewel.y + 1);
					if((state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
					{
						downEscaped = true;
						break;
					}
				}
				if(!downEscaped)
				{
					for(int i = 0; i < 10; i++)
					{
						//Then go left
						t = new Square(jewel.x - i, jewel.y);
						if(!(state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
						{
							if(jewel.y != 5 || jewel.x <= 4)
								System.out.println("Error Y2 in algo! " + down);
							return false;
						}
						t = new Square(jewel.x - i, jewel.y + 1);
						if((state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
						{
							break;
						}
					}
				}
			}
			
			if(!left)
			{				
				//Check if up is a hole, before reaching a wall
				boolean leftEscaped = false;
				Square t;
				for(int i = 0; i < 10; i++)
				{
					//first go up
					t = new Square(jewel.x, jewel.y - i);
					if(!(state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
					{
						if(jewel.x != 1)
							System.out.println("Error X in algo!" + up);
						return false;
					}
					t = new Square(jewel.x - 1, jewel.y - i);
					if(!(state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
					{
						leftEscaped = true;
						break;
					}
				}
				if(!leftEscaped)
				{
					for(int i = 0; i < 10; i++)
					{
						//Then go down
						t = new Square(jewel.x, jewel.y + i);
						if(!(state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
						{
							if(jewel.x != 1)
								System.out.println("Error X in algo!" + up);
							return false;
						}
						t = new Square(jewel.x - 1, jewel.y + i);
						if(!(state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
						{
							break;
						}
					}
				}
				
			}
			
			if(!right)
			{				
				//Check if up is a hole, before reaching a wall
				boolean rightEscaped = false;
				Square t;
				for(int i = 0; i < 10; i++)
				{
					//first go up
					t = new Square(jewel.x, jewel.y - i);
					if(!(state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
					{
						System.out.println("Error X in algo!" + up);
						return false;
					}
					t = new Square(jewel.x + 1, jewel.y - i);
					if(!(state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
					{
						rightEscaped = true;
						break;
					}
				}
				if(!rightEscaped)
				{
					for(int i = 0; i < 10; i++)
					{
						//Then go down
						t = new Square(jewel.x, jewel.y + i);
						if(!(state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
						{
							System.out.println("Error X in algo!" + up);
							return false;
						}
						t = new Square(jewel.x + 1, jewel.y + i);
						if(!(state.emptys.contains(t) || state.jewels.contains(t) || state.man.equals(t) || state.goals.contains(t)))
						{
							break;
						}
					}
				}
			}
			if(jewel.x == 1)
				System.out.println("Error X in algo!" + up);
			if(jewel.y == 1)
				System.out.println("Error Y1 in algo!" + up);
			if(jewel.y == 5 && jewel.x > 4)
				System.out.println("Error Y2 in algo! " + down);
			
//			if(jewel.x == 1)
//				return false;
//			if(jewel.y == 1)
//				return false;
//			if(jewel.y == 5 && jewel.x > 4)
//				return false;
			
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
