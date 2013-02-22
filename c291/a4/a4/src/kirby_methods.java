import java.util.regex.Pattern;
import java.util.HashMap;
import java.lang.Math;
import com.sleepycat.db.*;


public class kirby_methods {

	/*
	 *  Method parses a string according to the spec of assignment 4
	 *  Passed: a single line of the data file as a String
	 *  Returns: an array with as many elements as there are ratings for the song in the line,
	 *  		each element is a String[2], where the first is a comma separated "<songID>,<username>"
	 *  		and the second is "<rating>", so that each such pair is ready for key,data into bekeley db
	 *  
	 */
	public static String[][] parseLine(String dataLine) {
		//clean the line and remove the curly braces
		int len = dataLine.length();
		String clean = dataLine.trim().substring(1, len - 1);
		//get the song id
		int idStart = clean.indexOf("[") + 1;
		int idEnd = clean.indexOf("]", idStart);
		String id = clean.substring(idStart, idEnd);
		//ignore the song title and artist
		int titleEnd = clean.indexOf("]", idEnd + 1);
		int artistEnd = clean.indexOf("]", titleEnd + 1);
		//isolate the username,rating pairs
		int rateStart = clean.indexOf("[", artistEnd + 1) + 1;
		int rateEnd = clean.indexOf("]", rateStart);
		String[] rate = clean.substring(rateStart, rateEnd).split(Pattern.quote(")"));
		//prepare the Nx2 array to be loaded with key,data pairs
		int numberRatings = rate.length;
		String[][] pairs = new String[numberRatings][2];
		//load the return array
		int k = 0;
		for (String val : rate) {
			int start = val.indexOf("(") + 1;
			String[] pair = val.substring(start).split(Pattern.quote(","));
			pairs[k][0] = id + "," + pair[0].trim();
			pairs[k][1] = pair[1].trim(); 
			k = k+1;
		}

		return pairs;
	}
	
	/*
	 * 	takes an input song id and a berkdb instance with <song id>,<username> as key, and <rating> as data
	 */
	public static String top3(String id, Database db) {

		//initialize cursor and database entries for the linear scan
		Cursor cursor = null;
		try {
			cursor = db.openCursor(null, null);
		} catch (Exception e) {
			System.out.println("Error initializing cursor.\n" + e.getMessage());
		}
		DatabaseEntry key = new DatabaseEntry();
		DatabaseEntry data = new DatabaseEntry();

		//linear scan to find the rating data for the input song

		//initialize container to hold rating data for input song
		HashMap<String,Integer> inputRatings = new HashMap<String,Integer>();
		//set flags for locating songs in clustered rows
		boolean songFound = false;
		boolean songDone = false;
		
		try {
			while (cursor.getNext(key, data, LockMode.DEFAULT) == OperationStatus.SUCCESS && !songDone) {
				//parse the csv key entry into song id and user
				String[] idUser = key.getData().toString().split(",");
				if (id.equals(idUser[0])) {
					songFound = true;
					//append rating data
					inputRatings.put(idUser[1], Integer.parseInt(data.getData().toString()));
				} else if (songFound) {
					songDone = true;
				}
				//clear the key and data containers because berkdb is silly
				key.setData(null);
				data.setData(null);
			}

			//initialize the ids and distances to be replaced by the loop below
			String firstIDs = "";
			String secondIDs = "";
			String thirdIDs = "";
			double firstDist = 999;
			double secondDist = 999;
			double thirdDist = 999;
			//initialize containers for rating data for each song before distance calculation
			HashMap<String,Integer> currRatings = new HashMap<String,Integer>();
			boolean firstIter = true;
			String prevID = "default";
			while (cursor.getNext(key, data, LockMode.DEFAULT) == OperationStatus.SUCCESS) {
				//get rating data from current row
				String[] currIDUser = key.getData().toString().split(",");
				String currID = currIDUser[0];
				String currUser = currIDUser[1];
				int currRating = Integer.parseInt(data.getData().toString());
				if (!currID.equals(prevID) && !firstIter) {
					//calculate distance between input song and current song
					double currDist = distance(inputRatings, currRatings);

					//compare current song to input song
					if (currDist < firstDist) {
						//set thirdID and thirdDist
						thirdIDs = secondIDs;
						thirdDist = secondDist;
						//set secondID and secondDist
						secondIDs = firstIDs;
						secondDist = firstDist;
						//set firstID and firstDist
						firstIDs = currID;
						firstDist = currDist;
					} else if (currDist < secondDist) {
						//set thirdID and thirdDist
						thirdIDs = secondIDs;
						thirdDist = secondDist;
						//set secondID and secondDist
						secondIDs = firstIDs;
						secondDist = firstDist;
					} else if (currDist < thirdDist ) {
						//set thirdID and thirdDist
						thirdIDs = secondIDs;
						thirdDist = secondDist;
					} else if (currDist == firstDist) {
						//append fistID
						firstIDs += ", " + currID;
					} else if (currDist == secondDist) {
						//append secondID
						secondIDs += ", " + currID;
					} else if (currDist == thirdDist) {
						//append thirdID
						thirdIDs += ", " + currID;
					}
					//now moving to a new song, so clear the current song's hashmap
					currRatings.clear();
				} else {
					currRatings.put(currUser, currRating);
				}
				//clear the key and data containers because berkdb is silly
				key.setData(null);
				data.setData(null);
			}
			return id + ", " + firstIDs + ", " + secondIDs + ", " + thirdIDs;
			
		} catch (DatabaseException e) {
			System.out.println("Error in reading berkeley db instance.\n"+e.getMessage());
		}

		return null;
	}

	/*
	 * calculate euclidean distance between two songs based on common ratings
	 * returns max value if there are no common users
	 */
	private static double distance(HashMap<String,Integer> inputRatings, HashMap<String,Integer> currRatings) {
		int sqSum = 0;
		double dim = 0;
		for (String user : inputRatings.keySet()) {
			if (currRatings.containsKey(user)) {
				sqSum += Math.pow(inputRatings.get(user)-currRatings.get(user), 2);
				dim += 1;
			}
		}
		if (dim > 0) {
			return Math.sqrt((double) sqSum)/dim;
		} else {
			return Integer.MAX_VALUE;
		}
	}

}
