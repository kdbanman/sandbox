

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintStream;
import java.util.HashMap;

import com.sleepycat.db.*;


public class indexed {
	
	public static void start(Database std, String filename){
		
		//build hash tables
		long starttime;
		long performance = 0; //For measuring performance
		Database secDB = null;
		Database tDB = null;
		try{
			starttime = System.currentTimeMillis();
			System.out.print("Building <user>,<songs,ratings> secondary table...");
			secDB = buildsecondary(std);
			performance = System.currentTimeMillis() - starttime;
			System.out.println(" Complete! " + performance + "ms");

		}catch(Exception e){
			System.out.println(e.getMessage());
		}
		try{
			starttime = System.currentTimeMillis();
			System.out.print("Building <song>,<users> tertiary table...");
			tDB = buildtertiary(std);
			performance = System.currentTimeMillis() - starttime;
			System.out.println(" Complete! " + performance + "ms");

		}catch(Exception e){
			System.out.println("Error building secondary tables.");
			System.out.println(e.getMessage());
		}
		
		// QUERIES //
		//use hash tables to query fast!
		PrintStream writer = io.writer("indexedanswers.txt", false);
		BufferedReader qreader = io.reader(filename);
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
					System.out.print("Indexed... ");
					starttime = System.currentTimeMillis();
					send = top3(line, secDB, tDB);
					if(send != null)
						writer.println(send);
					else
						System.out.println("Error from ranking search function");
					performance = System.currentTimeMillis() - starttime;
					System.out.println(" Complete! " + performance + "ms");
				}
				if (performance > max) max = performance;
				if (performance < min) min = performance;
				total += performance;
				count +=1;
			}
			avg = total/count;
		}catch(IOException ioe){
			System.out.println(ioe.getMessage());
		}catch(Exception e){
			System.out.println("error querying for top 3 songs");
			System.out.println(e.getMessage());
		}
		
		System.out.println("Total querying time: "+Long.toString(total)+" ms (average: "+Long.toString(avg)+" ms/query). Fastest query: "+Long.toString(min)+" ms.  Slowest query: "+Long.toString(max)+" ms.");
		writer.close();

	}
	
	public static String rank(Database sqSumdb) throws DatabaseException {
	
		Cursor sqSumCurs = sqSumdb.openCursor(null, null);
		DatabaseEntry sqSumKey = new DatabaseEntry();
		DatabaseEntry sqSumData = new DatabaseEntry();
		
		//initialize the ids and distances to be replaced by the loop below
		String firstIDs = "";
		String secondIDs = "";
		String thirdIDs = "";
		double inf = Integer.MAX_VALUE;
		double firstDist = inf;
		double secondDist = inf;
		double thirdDist = inf;
		//initialize containers for rating data for each song before distance calculation
		boolean firstFilled = true;
		boolean secondFilled = true;
		boolean thirdFilled = true;
		while (sqSumCurs.getNext(sqSumKey, sqSumData, LockMode.DEFAULT) == OperationStatus.SUCCESS) {
			//get song id
			String id = (new String(sqSumKey.getData()));
			String[] sumN = (new String(sqSumData.getData())).split(",");
			sqSumKey.setData(null); sqSumData.setData(null);
			double sum = Integer.parseInt(sumN[0]);
			double N = Integer.parseInt(sumN[1]);
			double dist = Math.sqrt(sum)/N;
			
			if (dist != inf) {
				if (dist < firstDist || !firstFilled) {
					//set thirdID and thirdDist
					thirdIDs = secondIDs;
					thirdDist = secondDist;
					//set secondID and secondDist
					secondIDs = firstIDs;
					secondDist = firstDist;
					//set firstID and firstDist
					firstIDs = id;
					firstDist = dist;
					if (firstFilled) {
						if (secondFilled) {
							thirdFilled = true;
						}
						secondFilled = true;
					}
					firstFilled = true;
				} else if ((dist < secondDist || !secondFilled) && dist != firstDist) {
					//set thirdID and thirdDist
					thirdIDs = secondIDs;
					thirdDist = secondDist;
					//set secondID and secondDist
					secondIDs = id;
					secondDist = dist;
					if (secondFilled) {
						thirdFilled = true;
					}
					secondFilled = true;
				} else if ((dist < thirdDist || !thirdFilled) && dist != firstDist && dist != secondDist) {
					//set thirdID and thirdDist
					thirdIDs = id;
					thirdDist = dist;
					thirdFilled = true;
				} else if (dist == firstDist) {
					//append fistID
					firstIDs += ", " + id;
				} else if (dist == secondDist) {
					//append secondID
					secondIDs += ", " + id;
				} else if (dist == thirdDist) {
					//append thirdID
					thirdIDs += ", " + id;
				}
			}
		}
		if (firstIDs.equals("")) firstIDs = "<no 1st place>";
		if (secondIDs.equals("")) secondIDs = "<no 2nd place>";
		if (thirdIDs.equals("")) thirdIDs = "<no 3rd place>";
		
		return firstIDs + ", " + secondIDs + ", " + thirdIDs;
	}
	
	public static String top3(String line, Database secdb, Database tdb) throws DatabaseException, FileNotFoundException {
		//configure sqSum db for keeping track of cumulative squaresums
		io.deleteFile("sqSumdb");
		DatabaseConfig dbConfig = new DatabaseConfig();
		dbConfig.setType(DatabaseType.HASH);
		dbConfig.setAllowCreate(true);
		dbConfig.setUnsortedDuplicates(true);
		Database sqSumdb = new Database("sqSumdb", null, dbConfig);
		
		Cursor sqSumCurs = sqSumdb.openCursor(null, null);
		DatabaseEntry sqSumKey = new DatabaseEntry();
		DatabaseEntry sqSumData = new DatabaseEntry();
		
		Cursor secCurs = secdb.openCursor(null, null);
		Cursor tCurs = tdb.openCursor(null, null);
		DatabaseEntry secKey = new DatabaseEntry();
		DatabaseEntry secData = new DatabaseEntry();
		DatabaseEntry tKey = new DatabaseEntry();
		DatabaseEntry tData = new DatabaseEntry();
		
		// get input song users and ratings
		tKey.setData(line.getBytes());
		if (tCurs.getSearchKey(tKey, tData, LockMode.DEFAULT) == OperationStatus.SUCCESS) {
			// for each user in input song, get songs and ratings
			HashMap<String,String> iRatings = parseBrace(new String(tData.getData()));
			for (String user : iRatings.keySet()) {
				// get current user's rating for input song
				int inputRating = Integer.parseInt(iRatings.get(user));
				// get songs and ratings for user
				secKey.setData(null); secData.setData(null);
				secKey.setData(user.getBytes());
				if (secCurs.getSearchKey(secKey, secData, null) == OperationStatus.SUCCESS) {
					//for each song rated by user
					HashMap<String,String> currSongs = parseBrace(new String(secData.getData()));
					for (String song : currSongs.keySet()) {
						// input song should not be compared to itself, otherwise get the users and ratings for it
						if (song.equals(line)) continue;
						// current user's rating for song under inspection
						int songRating = Integer.parseInt(currSongs.get(song));
						sqSumKey.setData(null); sqSumData.setData(null);
						sqSumKey.setData(song.getBytes());
						if (sqSumCurs.getSearchKey(sqSumKey, sqSumData, null) == OperationStatus.SUCCESS) {
							// if song is already in sqSum,N db, add to it
							String[] sumN = (new String(sqSumData.getData())).split(",");
							
							// add the new square sum to the previous and increment N
							int sum = Integer.parseInt(sumN[0]);
							int N = Integer.parseInt(sumN[1]);
							sum += (inputRating-songRating)*(inputRating-songRating);
							N += 1;
							String encoded = Integer.toString(sum) + "," + Integer.toString(N);
							
							// remove old entry for current song and replace it with the new one
							sqSumCurs.delete();
							sqSumKey.setData(null); sqSumData.setData(null);
							sqSumKey.setData(song.getBytes()); sqSumData.setData(encoded.getBytes());
							sqSumdb.put(null, sqSumKey, sqSumData);
							
						} else {
							// if song in not already in sqSum,N db, create it
							int sum = (inputRating-songRating)*(inputRating-songRating);
							int N = 1;
							String encoded = Integer.toString(sum) + "," + Integer.toString(N);
							sqSumKey.setData(null); sqSumData.setData(null);
							sqSumKey.setData(song.getBytes()); sqSumData.setData(encoded.getBytes());
							sqSumdb.put(null, sqSumKey, sqSumData);
						}
					}
				} else {
					System.out.println("ERROR:  user "+user+" not in secondary database.");
				}
				
			}
		} else {
			return line + " has not been rated by any user.";
		}
		//DEBUG
		//io.debugread(sqSumdb);
		
		// calculate distance for each song in, inserting into the top 3 spots as we iterate through
		String ranked = rank(sqSumdb);
		return line + ", " +ranked;
	}
	
	public static Database buildtertiary(Database std) {
		
		try{
			//configure new database instance
			io.deleteFile("tertiarydb");
			DatabaseConfig dbConfig = new DatabaseConfig();
			dbConfig.setType(DatabaseType.HASH);
			dbConfig.setAllowCreate(true);
			dbConfig.setUnsortedDuplicates(true);
			Database tdb = new Database("tertiarydb", null, dbConfig);
			
			//configure cursors and entries
			Cursor stdCurs = std.openCursor(null, null);
			Cursor tCurs = tdb.openCursor(null, null);
			DatabaseEntry stdKey = new DatabaseEntry();
			DatabaseEntry stdData = new DatabaseEntry();
			DatabaseEntry tKey = new DatabaseEntry();
			DatabaseEntry tData = new DatabaseEntry();
			
			//extract from linearly constructed database to populate <song>,<users> table, making
			//use of songs grouped by id
			String currUsers = "";
			String prevID = "default";
			boolean firstIter = true;
			while (stdCurs.getNext(stdKey, stdData, LockMode.DEFAULT) == OperationStatus.SUCCESS) {
				//get rating data from current row
				String[] currIDUser = (new String(stdKey.getData())).split(",");
				String currID = currIDUser[0].trim();
				String currUser = currIDUser[1].trim();
				String currRating = (new String(stdData.getData()));
				stdKey.setData(null);
				stdData.setData(null);
				if (currID.equals(prevID) || firstIter) {
					//concatenate new username with current string
					currUsers += "("+currUser+","+currRating+")";
				} else if (!firstIter) {
					//insert completed <usernames> into table under key <song id>
					tKey.setData(prevID.getBytes());
					tData.setData(currUsers.substring(0, currUsers.length()).getBytes());
					tCurs.put(tKey, tData);
					tKey.setData(null);
					tData.setData(null);
					//DEBUG:
					//System.out.println(prevID+","+currUsers.substring(0, currUsers.length()-1));
					//start the new <usernames> for the next song (in currID)
					currUsers = "("+currUser+","+currRating+")";
				}
				prevID = currID;
				firstIter = false;
			}
			//repeat iteration for last song
			tKey.setData(prevID.getBytes());
			tData.setData(currUsers.substring(0, currUsers.length()).getBytes());
			tCurs.put(tKey, tData);
			tKey.setData(null);
			tData.setData(null);
			
			//DEBUG:
			//io.debugread(tdb);
			tCurs.close();
			
			return tdb;
			
		} catch (Exception e) {
			System.out.println(" error creating <song>,<users> tertiary table\n");
			System.out.println(e.getMessage());
		}
		return null; //should never happen
		
	}
	
	public static Database buildsecondary(Database std){
		//Parse database loaded
		try{
			io.deleteFile("secondarydb");
			// SecondaryDatabases started
			DatabaseConfig dbConfig = new DatabaseConfig();
			dbConfig.setType(DatabaseType.HASH);
			dbConfig.setAllowCreate(true);
			dbConfig.setUnsortedDuplicates(true);
			Database secdb = new Database("secondarydb", null, dbConfig);
			//Cursors started
			Cursor stdcursor = std.openCursor(null, null);
			Cursor secdbcursor = secdb.openCursor(null, null);
			//Key and Data started
			DatabaseEntry stdkey = new DatabaseEntry();
			DatabaseEntry stddata = new DatabaseEntry();
			DatabaseEntry seckey = new DatabaseEntry();
			DatabaseEntry secdata = new DatabaseEntry();

			while(stdcursor.getNext(stdkey, stddata, LockMode.DEFAULT) == OperationStatus.SUCCESS){//Writing into secondary db
				String[] key = new String(stdkey.getData()).split(",");
				String data = new String(stddata.getData());
				//DEBUG:
				//System.out.println("key 0:" + key[0] + " key 1:" + key[1] + " data:" + data);
				seckey.setData(key[1].getBytes());
				OperationStatus operation = secdbcursor.getSearchKey(seckey, secdata, LockMode.DEFAULT);

				String b = null;
				while(operation == OperationStatus.SUCCESS){
					b = new String(secdata.getData());
					secdbcursor.delete();
					operation = secdbcursor.getNextDup(seckey, secdata, LockMode.DEFAULT);
				}
				if(b == null){
					seckey.setData(key[1].getBytes());
					secdata.setData(("("+key[0]+","+data+")").getBytes());
					secdb.put(null, seckey, secdata);
				}
				if(b != null){
					secdata.setData(b.concat("("+key[0]+","+data+")").getBytes());
					secdb.put(null, seckey,secdata);
				}
				seckey.setData(null);
				secdata.setData(null);

				stdkey.setData(null);
				stddata.setData(null);
			}
			//io.debugread(secdb);

			return secdb;
		}catch(Exception e){
			System.out.println("Error creating <user>,<song,rating> secondary table!\n");
			System.out.println(e.getMessage());
		}
		return null; //SHOULD NEVER HAPPEN
	}
	
	public static HashMap<String, String> parseBrace(String unparsed) {
		HashMap<String,String> parsed = new HashMap<String,String>();
		try {
			String[] split = unparsed.substring(1, unparsed.length()-1).split("\\)\\(");
			for (String pair : split) {
				String[] both = pair.split(",");
				parsed.put(both[0], both[1]);
			}
		}catch (Exception e){
			System.out.println("ERROR: parenthetically parsed data not properly formatted");
		}
		return parsed;
	}
}
