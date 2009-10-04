package sokoban;

import java.util.ArrayList;

public class SokobanState implements Cloneable
{
	public ArrayList<Square> emptys = new ArrayList<Square>();
	public ArrayList<Square> goals = new ArrayList<Square>();
	public ArrayList<Square> jewels = new ArrayList<Square>();
	public char moveAction;
	public SokobanState parentState = null;
	public Square man;
	public int manMoveLength = 0;
	public int score = Integer.MAX_VALUE;
	
	@Override 
	public Object clone() throws CloneNotSupportedException
	{
		SokobanState stateClone = (SokobanState)super.clone();
		stateClone.emptys = copyList(this.emptys);
		stateClone.goals = copyList(this.goals);
		stateClone.jewels = copyList(this.jewels);
		stateClone.moveAction = this.moveAction;
		stateClone.man = this.man;
		stateClone.score = this.score;
		stateClone.parentState = this.parentState;
		stateClone.manMoveLength = this.manMoveLength;
		return stateClone;
	}
	
	private ArrayList<Square> copyList(ArrayList<Square> src)
	{
		ArrayList<Square> lst = new ArrayList<Square>();
		for(Square element : src)
		{
			try
			{
				lst.add((Square)element.clone());
			}
			catch (CloneNotSupportedException e)
			{
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		return lst;
	}
	@Override 
	public boolean equals(Object other)
	{
		if(this == other)
			return true;
		if(!(other instanceof SokobanState))
			return false;
		
		SokobanState that = (SokobanState)other;
		if(this.jewels.containsAll(that.jewels))
		{
			if(this.man.equals(that.man))
			{
				return true;
			}
		}
		return false;
	}
}
