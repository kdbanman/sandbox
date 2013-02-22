import java.util.Vector;
import java.sql.*;


public class four {

	public static void menu(String username, Connection m_con) throws SQLException{
		Vector<String> movies_owned = new Vector<String>();
		Vector<String> ids = new Vector<String>();
		String query = "(select id, title from media, buy where username='"+username+"' and mediaid=id) union "
					 + "(select id, title from media, rent where username='"+username+"' and movieid=id)";
		Statement stmt = InputOutput.newStatement(m_con);
		ResultSet rs = InputOutput.execQuery(stmt, query);
		while (rs.next()) {
			String id = rs.getString("id").trim();
			ids.add(id);
			while (id.length() < 21) {
				id = id + " ";
			}
			String title = rs.getString("title").trim();
			movies_owned.add(id + title);
		}
		InputOutput.closeStatement(stmt);
		int back = 0;
		while(back == 0){
			InputOutput.clearscreen();
			System.out.println("**************************");
			System.out.println("* Movies owned or rented *");
			System.out.println("**************************\n");
			System.out.println("   MOVIE ID           TITLE\n");
			InputOutput.vectorPrint(movies_owned);
			System.out.print("\n1. Rate Movie\n2. Home\nChoice: ");
			
			int command = InputOutput.cleanCommand(InputOutput.read());
			
			switch (command){
				case 1:
					rate(username, m_con);
					InputOutput.clearscreen();
					break;
				case 2:
					back = 1;
					InputOutput.clearscreen();
					break;
				default:
					InputOutput.invalidcom();
					break;
			}
		}
	}
	private static void rate(String username, Connection m_con) throws SQLException{
		
		int answered = 0;
		int rating = 0;
		while(answered == 0){
			Vector<String> rateable = new Vector<String>();
			Vector<String> ids = new Vector<String>();
			String query = "((select id, title from media, buy, movie where username='"+username+"' and mediaid=id and mid=id) union "
						 + "(select id, title from media, rent where username='"+username+"' and movieid=id)) minus "
						 + "(select movieid id, title from media, rate where username='"+username+"' and movieid=id)";
			Statement stmt = InputOutput.newStatement(m_con);
			ResultSet rs = InputOutput.execQuery(stmt, query);
			while (rs.next()) {
				String id = rs.getString("id").trim();
				ids.add(id);
				while (id.length() < 21) {
					id = id + " ";
				}
				String title = rs.getString("title").trim();
				rateable.add(id + title);
			}
			InputOutput.closeStatement(stmt);
			InputOutput.clearscreen();
			System.out.println("****************");
			System.out.println("* Rate a movie *");
			System.out.println("****************\n");
			System.out.println("   MOVIE ID           TITLE\n");
			InputOutput.vectorPrint(rateable);;
			System.out.print("Movie id to rate (only movies not rated by you are shown): ");
			String mid = InputOutput.read();
			
			if(!ids.contains(mid)){
				InputOutput.invalidcom();
			}
			else
			{
				System.out.print("\nWhat is your rating for it? (0-10): ");
				
				rating = InputOutput.cleanCommand(InputOutput.read());
				if(rating >= 0 && rating <=10)// Check rating
				{
					rateMovie(username, mid, rating, m_con);
					System.out.println("Movie rated! Thanks!");
					InputOutput.threadsleep(3000);
					answered = 1;
				}
				else{
					InputOutput.invalidcom();
					answered = 0;
					InputOutput.threadsleep(3000);
				}
			}
		}

	}
	
	private static void rateMovie(String username, String mid, int rating, Connection m_con) {
		String query = "insert into rate values ('"+username+"','"+mid+"','"+(rating)+"')";
		Statement stmt = InputOutput.newStatement(m_con);
		InputOutput.execUpdate(stmt, query);
		InputOutput.closeStatement(stmt);
	}
}

