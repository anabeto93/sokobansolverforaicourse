package sokoban;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class MapParser
{

	private int maxMapLength;
	private int maxMapHeight;
	private char[][] mapArray;

	public MapParser()
	{
	}

	private ArrayList<String> getRawMapData(File mapFile)
	{
		ArrayList<String> content = new ArrayList<String>();
		try
		{
			BufferedReader lineReader = new BufferedReader(new FileReader(mapFile));
			String line = null;
			while ((line = lineReader.readLine()) != null)
			{
				content.add(line);
			}
		}
		catch (FileNotFoundException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		catch (IOException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return content;
	}

	public SokobanState getInitialSokobanState(String pathToMap)
	{
		SokobanState initialState = new SokobanState();
		File mapFile = new File(pathToMap);
		ArrayList<String> rawMap = getRawMapData(mapFile);		
		
		maxMapLength = 0;
		maxMapHeight = 0;
		for(String line : rawMap)
		{
			if(line.length() > maxMapLength)
			{
				maxMapLength = line.length();
			}
			if(line.contains("X"))
			{
				maxMapHeight++;
			}
		}
		mapArray = new char[maxMapHeight][maxMapLength];
		int lineIndex = 0;
		for(String line : rawMap)
		{
			if(line.contains("X"))
			{
				if(line.length() < maxMapLength)
				{
					int appendAmount = maxMapLength - line.length();
					for(int i = 0; i < appendAmount; i++)
					{
						line += " ";
					}
				}
				mapArray[lineIndex] = line.toCharArray(); 
				lineIndex++;
			}
		}
		
		//Now we can initialize the state
		for(int x = 0; x < maxMapLength; x++)
		{
			for(int y = 0; y < maxMapHeight; y++)
			{
				switch(mapArray[y][x])
				{
				case 'J':
					initialState.jewels.add(new Square(x, y));
					break;
				case 'G':
					initialState.goals.add(new Square(x, y));
					initialState.emptys.add(new Square(x, y));
					break;
				case '.':
					initialState.emptys.add(new Square(x, y));
					break;
				case 'M':
					initialState.man = new Square(x, y);
					break;
				default:
					break;
				}
			}
		}
		
		return initialState;
	}
	
	public void printMap(SokobanState state)
	{
		String line;
		//Now we can initialize the state
		for(int y = 0; y < maxMapHeight; y++)
		{
			line = "";
			for(int x = 0; x < maxMapLength; x++)
			{
				if(state.man.equals(new Square(x, y)))
				{
					line += "M";
				}
				else if(state.jewels.contains(new Square(x, y)))
				{
					line += "J";
				}
				else if(state.goals.contains(new Square(x, y)))
				{
					line += "G";
				}
				else
				{
					if(mapArray[y][x] == 'X')
					{
						line += mapArray[y][x];
					}
					else
					{
						line += ".";
					}
					
				}
			}
			System.out.println(line);
		}
	}

}
