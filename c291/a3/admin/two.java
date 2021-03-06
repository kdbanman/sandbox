import java.sql.*;
import java.util.Vector;

public class two {
	public static void menu(Connection m_con) throws SQLException{
		Statement stmt = InputOutput.newStatement(m_con);
		int back = 0;
		while(back == 0){
			int threshold = 1;
			int amount = 1;
			boolean displayed = false;
			while (threshold >= 0 && threshold <= 10 && amount >= 1 && !displayed) {
				prettyTop();
				System.out.print("Rating threshold? (0-10) ");
				threshold = InputOutput.cleanCommand(InputOutput.read());
				System.out.print("Amount of movies? ");
				amount = InputOutput.cleanCommand(InputOutput.read());

				if (threshold < 0 || threshold > 10) {
					System.out.println("ERROR!!  Threshold must be be integer 0-10");
					InputOutput.threadsleep(3000);
					break;
				} else if (amount < 1) {
					System.out.println("ERROR!!  Amount must be integer > 0");
					InputOutput.threadsleep(3000);
					break;
				}
				
				String query = "select movieid, title, rating from media, rate where id=movieid and rating>"+(threshold)+" order by rating desc";
				ResultSet rs = stmt.executeQuery(query);
				
				boolean tooMany = false;
				Vector<String> results = new Vector<String>();
				for (int i=0; i<amount; i++) {
					if (rs.next()) {
						String mid = rs.getString("movieid");
						while (mid.length() < 21) {
							mid = mid + " ";
						}
						String title = rs.getString("title");
						while (title.length() < 21) {
							title = title + " ";
						}
						String rating = rs.getString("rating");
						String printRow = mid + title + rating;
						results.add(printRow);
					} else {
						System.out.println("ERROR!!  Too few movies above rating threshold");
						tooMany = true;
						InputOutput.threadsleep(3000);
						break;
					}
				}
				
				if (!tooMany) {
					System.out.println("MOVIE ID            MOVIE TITLE         RATING");
					InputOutput.vectorPrint(results);
					System.out.println("");
					displayed = true;
					
					System.out.print("Press enter to return to home screen.");
					InputOutput.read();
					back = 1;
					break;
				}
				
			}


		}
		InputOutput.closeStatement(stmt);
	}
	
	private static void prettyTop() {
		InputOutput.clearscreen();
		System.out.println("******************************");
		System.out.println("*      View top movies       *");
		System.out.println("******************************\n");
	}
}
