package sokoban;

import java.util.ArrayList;

public class ManPathfinder extends AStarSearch
{
	@Override
	public int evaluateState(SokobanState state, SokobanState stateGoal)
	{
		return Math.abs(state.man.x - stateGoal.man.x) + Math.abs(state.man.y - stateGoal.man.y);
	}

	@Override
	public ArrayList<SokobanState> expandFringe(SokobanState state)
	{
		ArrayList<SokobanState> fringe = new ArrayList<SokobanState>();
		
		try
		{
			Square[] moves = new Square[4];
			//Up
			moves[0] = new Square(state.man.x, state.man.y - 1);
			//Down
			moves[1] = new Square(state.man.x, state.man.y + 1);
			//Left
			moves[2] = new Square(state.man.x - 1, state.man.y);
			//Right
			moves[3] = new Square(state.man.x + 1, state.man.y);			
			
			for(Square direction : moves)
			{
				if(!state.jewels.contains(direction) && state.emptys.contains(direction))
				{
					SokobanState stateNew;
					stateNew = (SokobanState)state.clone();		
					stateNew.man = (Square)direction.clone();
					stateNew.parentState = state;
					fringe.add(stateNew);
				}
			}
		}
		catch (CloneNotSupportedException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return fringe;
	}

	@Override
	public boolean isValid(SokobanState state)
	{
		return true;
	}

	@Override
	public boolean isGoalState(SokobanState state, SokobanState stateGoal)
	{
		return state.man.equals(stateGoal.man);
	}

	@Override
	public void infoFunction()
	{
		// TODO Auto-generated method stub
		
	}

}
