package sokoban;

public class Square implements Cloneable
{
	public int x;
	public int y;
	
	public Square(int x, int y)
	{
		this.x = x;
		this.y = y;
	}
	
	@Override 
	public boolean equals(Object other)
	{
		if(this == other)
			return true;
		if(!(other instanceof Square))
			return false;
		
		Square that = (Square)other;
		if(this.x == that.x && this.y == that.y)
			return true;
			
		return false;
	} 
	
	@Override 
	public int hashCode()
	{
		return (this.y << 16) + this.x;
	}

	@Override 
	public Object clone() throws CloneNotSupportedException
	{
		Square stateClone = (Square)super.clone();
		stateClone.x = this.x;
		stateClone.y = this.y;
		return stateClone;
		
	}
}
