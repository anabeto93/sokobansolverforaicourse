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

	protected SokobanState stateGoal;
	protected SokobanState stateInitial;

	protected char upDirection = 'u';
	protected char downDirection = 'd';
	protected char leftDirection = 'l';
	protected char rightDirection = 'r';

	private class ScoreComparator implements Comparator<SokobanState>
	{
		@Override
		public int compare(SokobanState o1, SokobanState o2)
		{
			return o1.score - o2.score;
		}

	}

	public ArrayList<SokobanState> constructPathToGoal()
	{
		ArrayList<SokobanState> steps = new ArrayList<SokobanState>();
		SokobanState currentState = stateGoal;
		while (currentState != stateInitial)
		{
			if (!currentState.equals(currentState.parentState)) steps.add(0, currentState);
			currentState = currentState.parentState;
		}
		steps.add(0, currentState);
		return steps;
	}

	public boolean search(SokobanState stateInitial, SokobanState stateGoal)
	{
		this.stateGoal = stateGoal;
		this.stateInitial = stateInitial;
		openList = new ArrayList<SokobanState>();
		closedList = new ArrayList<SokobanState>();
		ScoreComparator comparator = new ScoreComparator();
		openList.add(stateInitial);
		while (true)
		{
			infoFunction();
			Collections.sort(openList, comparator);
			SokobanState stateCurrent = openList.remove(0);
			closedList.add(stateCurrent);
			ArrayList<SokobanState> fringe = expandFringe(stateCurrent);
			for (SokobanState stateFringe : fringe)
			{
				if (isValid(stateFringe))
				{
					if (isGoalState(stateFringe, stateGoal))
					{
						stateGoal.parentState = stateFringe;
						return true;
					}
					stateFringe.score = evaluateState(stateFringe, stateGoal);
					if (openList.contains(stateFringe))
					{
						SokobanState stateOld = openList.get(openList.indexOf(stateFringe));
						if (stateFringe.score < stateOld.score)
						{
							openList.set(openList.indexOf(stateOld), stateFringe);
						}
					}
					else
					{
						if (!closedList.contains(stateFringe))
						{
							openList.add(stateFringe);
						}
					}
				}
			}
			if (openList.size() == 0)
			{
				return false;
			}
		}
	}
}
