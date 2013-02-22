import java.io.*;


import java.util.HashMap;
import java.lang.Math;
import com.sleepycat.db.*;


public class linear
{
	public static void start(Database std, String filename){
		BufferedReader qreader = io.reader(filename);

		PrintStream writer = io.writer("linearanswers.txt", false);

		long starttime;
		long performance = 0; //For measuring performance
		String line, send;
		long max = 0;
		long min = Integer.MAX_VALUE;
		long total = 0;
		long count = 0;
		long avg = 0;
		try{
			while((line = qreader.readLine()) != null)
			{
				line = line.trim();
				if (line.equals("")) continue;
				if (!line.equals("")) {
					System.out.print("Linear... ");
					starttime = System.currentTimeMillis();
					send = top3(line, std);
					if(send != null)
						writer.println(send);
					else
						System.out.println("Error from linear search function");
					performance = System.currentTimeMillis() - starttime;
					System.out.println(" Complete! " + performance + "ms");
					
					if (performance > max) max = performance;
					if (performance < min) min = performance;
					total += performance;
					count +=1;
				}
				avg = total/count;
			}
		}catch(IOException ioe){
			System.out.println(ioe.getMessage());
		}
		System.out.println("Total querying time: "+Long.toString(total)+" ms (average: "+Long.toString(avg)+" ms/query). Fastest query: "+Long.toString(min)+" ms.  Slowest query: "+Long.toString(max)+" ms.");
		writer.close();

	}

	/*
	 * 	takes an input song id and a berkdb instance with <song id>,<username> as key, and <rating> as data
	 */
	public static String top3(String id, Database db) {

		//initialize cursor and database entries for the linear scan
		try {
			Cursor cursor = db.openCursor(null, null);

			DatabaseEntry key = new DatabaseEntry();
			DatabaseEntry data = new DatabaseEntry();

			//linear scan to find the rating data for the input song

			//initialize container to hold rating data for input song
			HashMap<String,Integer> inputRatings = new HashMap<String,Integer>();
			//set flags for locating songs in clustered rows
			boolean songFound = false;
			boolean songDone = false;

			while (cursor.getNext(key, data, LockMode.DEFAULT) == OperationStatus.SUCCESS && !songDone) {
				//parse the csv key entry into song id and user
				String[] idUser = (new String(key.getData())).split(",");
				if (id.equals(idUser[0])) {
					songFound = true;
					//append rating data
					inputRatings.put(idUser[1], Integer.parseInt(new String(data.getData())));
				} else if (songFound) {
					songDone = true;
				}
				//clear the key and data containers because berkdb is silly
				key.setData(null);
				data.setData(null);
			}
			cursor.close();
			cursor = db.openCursor(null, null);
			key.setData(null);
			data.setData(null);

			/**
			 * the code below looks like a long unmodularized mess because it was written with
			 * efficiency as the primary concern
			 */
			
			//initialize the ids and distances to be replaced by the loop below
			String firstIDs = "";
			String secondIDs = "";
			String thirdIDs = "";
			double inf = Integer.MAX_VALUE;
			double firstDist = inf;
			double secondDist = inf;
			double thirdDist = inf;
			//initialize containers for rating data for each song before distance calculation
			HashMap<String,Integer> currRatings = new HashMap<String,Integer>();
			boolean firstIter = true;
			boolean firstFilled = true;
			boolean secondFilled = true;
			boolean thirdFilled = true;
			String prevID = "default";
			while (cursor.getNext(key, data, LockMode.DEFAULT) == OperationStatus.SUCCESS) {
				//get rating data from current row
				String[] currIDUser = (new String(key.getData())).split(",");
				String currID = currIDUser[0];
				if (currID.equals(id)) {
					key.setData(null);
					data.setData(null);
					continue;
				}
				String currUser = currIDUser[1];
				int currRating = Integer.parseInt(new String(data.getData()));
				
//				DEBUG:  test acquisition of a single song's data
//				if (currID.equals("1316")) {
//					System.out.println(currID + " " + currUser + " " + currRating);
//				}
				
				if (!currID.equals(prevID) && !firstIter) {
					//calculate distance between input song and current song
					double currDist = distance(inputRatings, currRatings);
					
//					DEBUG:  if a song has a distance of zero w.r.t. the input, print its ratings and
//					  		mark the usernames in common. 
//					if (currDist == 0.0) {
//					 
//						System.out.println("\nSong ID " + prevID + ":");
//						for (String val : currRatings.keySet()) {
//							System.out.print(val + "," + currRatings.get(val));
//							if (inputRatings.containsKey(val)) System.out.print("   **");
//							System.out.println(" ");
//						}
//						System.out.println(" ");
//					}
					
					//compare current song to input song
					if (currDist != inf) {
						if (currDist < firstDist || !firstFilled) {
							//set thirdID and thirdDist
							thirdIDs = secondIDs;
							thirdDist = secondDist;
							//set secondID and secondDist
							secondIDs = firstIDs;
							secondDist = firstDist;
							//set firstID and firstDist
							firstIDs = prevID;
							firstDist = currDist;
							if (firstFilled) {
								if (secondFilled) {
									thirdFilled = true;
								}
								secondFilled = true;
							}
							firstFilled = true;
						} else if ((currDist < secondDist || !secondFilled) && currDist != firstDist) {
							//set thirdID and thirdDist
							thirdIDs = secondIDs;
							thirdDist = secondDist;
							//set secondID and secondDist
							secondIDs = prevID;
							secondDist = currDist;
							if (secondFilled) {
								thirdFilled = true;
							}
							secondFilled = true;
						} else if ((currDist < thirdDist || !thirdFilled) && currDist != firstDist && currDist != secondDist) {
							//set thirdID and thirdDist
							thirdIDs = prevID;
							thirdDist = currDist;
							thirdFilled = true;
						} else if (currDist == firstDist) {
							//append fistID
							firstIDs += ", " + prevID;
						} else if (currDist == secondDist) {
							//append secondID
							secondIDs += ", " + prevID;
						} else if (currDist == thirdDist) {
							//append thirdID
							thirdIDs += ", " + prevID;
						}
					}
					//now moving to a new song, so clear the current song's hashmap
					currRatings.clear();
					currRatings.put(currUser, currRating);
				} else {
					currRatings.put(currUser, currRating);
				}
				//clear the key and data containers because berkdb is silly
				key.setData(null);
				data.setData(null);
				
				prevID = currID;
				firstIter = false;
			}
			//perform calculation and insertion on final song
			double currDist = distance(inputRatings, currRatings);
			//compare current song to input song
			if (currDist != inf) {
				if (currDist < firstDist || !firstFilled) {
					//set thirdID and thirdDist
					thirdIDs = secondIDs;
					thirdDist = secondDist;
					//set secondID and secondDist
					secondIDs = firstIDs;
					secondDist = firstDist;
					//set firstID and firstDist
					firstIDs = prevID;
					firstDist = currDist;
					if (firstFilled) {
						if (secondFilled) {
							thirdFilled = true;
						}
						secondFilled = true;
					}
					firstFilled = true;
				} else if ((currDist < secondDist || !secondFilled) && currDist != firstDist) {
					//set thirdID and thirdDist
					thirdIDs = secondIDs;
					thirdDist = secondDist;
					//set secondID and secondDist
					secondIDs = prevID;
					secondDist = currDist;
					if (secondFilled) {
						thirdFilled = true;
					}
					secondFilled = true;
				} else if ((currDist < thirdDist || !thirdFilled) && currDist != firstDist && currDist != secondDist) {
					//set thirdID and thirdDist
					thirdIDs = prevID;
					thirdDist = currDist;
					thirdFilled = true;
				} else if (currDist == firstDist) {
					//append fistID
					firstIDs += ", " + prevID;
				} else if (currDist == secondDist) {
					//append secondID
					secondIDs += ", " + prevID;
				} else if (currDist == thirdDist) {
					//append thirdID
					thirdIDs += ", " + prevID;
				}
			}
			if (firstIDs.equals("")) firstIDs = "<no 1st place>";
			if (secondIDs.equals("")) secondIDs = "<no 2nd place>";
			if (thirdIDs.equals("")) thirdIDs = "<no 3rd place>";
			
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
		double sqSum = 0;
		int inCommon = 0;
		for (String user : inputRatings.keySet()) {
			if (currRatings.containsKey(user)) {
				inCommon += 1;
				sqSum += Math.pow(inputRatings.get(user)-currRatings.get(user), 2);
			}
		}
		if (inCommon > 0) {
			return Math.sqrt(sqSum)/inCommon;
		} else {
			return Integer.MAX_VALUE;
		}
	}


}