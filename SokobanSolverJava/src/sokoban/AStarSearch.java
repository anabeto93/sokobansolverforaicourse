package sokoban;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public abstract class AStarSearch
{
	protected ArrayList<SokobanState> openList;
	protected ArrayList<SokobanState> closedList;
	
	public abstract ArrayList<SokobanState> expandFringe(SokobanState state);
	public abstract int evaluateState(SokobanState state, SokobanState stateGoal);
	public abstract boolean isValid(SokobanState state);
	public abstract boolean isGoalState(SokobanState state, SokobanState stateGoal);
	public abstract void infoFunction();
	
	private SokobanState stateGoal;
	private SokobanState stateInitial;
	
	private class ScoreComparator implements Comparator<SokobanState>
	{
		@Override
		public int compare(SokobanState o1, SokobanState o2)
		{
			return o1.score - o2.score;
		}
		
	}
	
	public ArrayList<Character> getAllMovesToState()
	{
		ArrayList<Character> moves = new ArrayList<Character>();
		SokobanState currentState = stateGoal;
		while(currentState != stateInitial)
		{
			moves.add(0, currentState.moveAction);
			currentState = currentState.parentState;
		}
		return moves;		
	}
	
	public ArrayList<SokobanState> constructPathToGoal()
	{
		ArrayList<SokobanState> steps = new ArrayList<SokobanState>();
		SokobanState currentState = stateGoal;
		while(currentState != stateInitial)
		{
			steps.add(0, currentState);
			currentState = currentState.parentState;
		}
		return steps;
	}
	
	public boolean search(SokobanState stateInitial, SokobanState stateGoal)
	{
		openList = new ArrayList<SokobanState>();
		closedList = new ArrayList<SokobanState>();
		ScoreComparator comparator = new ScoreComparator();
		openList.add(stateInitial);
		while(true)
		{
			infoFunction();
			Collections.sort(openList, comparator);
			SokobanState stateCurrent = openList.remove(0);
			closedList.add(stateCurrent);
			ArrayList<SokobanState> fringe = expandFringe(stateCurrent);
			for(SokobanState stateFringe : fringe)
			{
				if(isValid(stateFringe))
				{
					if(isGoalState(stateFringe, stateGoal))
					{
						stateGoal.parentState = stateFringe;
						this.stateGoal = stateGoal;
						this.stateInitial = stateInitial;
						return true;
					}
					stateFringe.score = evaluateState(stateFringe, stateGoal);
					if(openList.contains(stateFringe))
					{
						SokobanState stateOld = openList.get(openList.indexOf(stateFringe));
						if(stateFringe.score < stateOld.score)
						{
							openList.set(openList.indexOf(stateOld), stateFringe);
						}
					}
					else
					{
						if(!closedList.contains(stateFringe))
						{
							openList.add(stateFringe);
						}
					}
				}
			}
			if(openList.size() == 0)
			{
				return false;
			}
		}
	}
}
