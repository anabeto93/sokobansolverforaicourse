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
			char[] action = new char[4];
			
			//Up
			moves[0] = new Square(state.man.x, state.man.y - 1);
			action[0] = 'u';
			
			//Down
			moves[1] = new Square(state.man.x, state.man.y + 1);
			action[1] = 'd';
			
			//Left
			moves[2] = new Square(state.man.x - 1, state.man.y);
			action[2] = 'l';
			
			//Right
			moves[3] = new Square(state.man.x + 1, state.man.y);			
			action[3] = 'r';
			
			for(int i = 0; i < 4; i++)
			{
				if(!state.jewels.contains(moves[i]) && state.emptys.contains(moves[i]))
				{
					SokobanState stateNew;
					stateNew = (SokobanState)state.clone();		
					stateNew.man = (Square)moves[i].clone();
					stateNew.parentState = state;
					stateNew.moveAction = action[i];
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
	
	public String getMoves()
	{
		StringBuilder moves = new StringBuilder();
		SokobanState searcher = this.stateGoal;
		while(!searcher.equals(this.stateInitial))
		{
			if(searcher.moveAction != ' ')
				moves.append(searcher.moveAction);
			searcher = searcher.parentState;
		}
		if(searcher.moveAction != ' ')
			moves.append(searcher.moveAction);
		moves.reverse();
		return moves.toString();
	}

}
