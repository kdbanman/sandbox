import java.util.*;
import java.sql.*;


public class one {
	public static void menu(Connection m_con) throws SQLException{
		Statement stmt = InputOutput.newStatement(m_con);
		int back = 0;
		while(back == 0){
			Vector<String> overdue = null;
			try {
				overdue = viewOverdue(stmt);
			}catch(Exception e){
				System.out.println(e.getMessage());
			}
			prettyUpdate(overdue);
			String command = InputOutput.read();
			int intCommand = InputOutput.cleanCommand(command);
			switch (intCommand){
			case 1:
				fixOverdue(m_con);
			case 2:
				back = 1;
				break;
			default:
				InputOutput.invalidcom();
				InputOutput.threadsleep(3000);
				break;
			}


		}
		InputOutput.closeStatement(stmt);
	}
	
	private static Vector<String> viewOverdue(Statement stmt) throws SQLException {
		String query = "select title, username, movieid from Rent, Media where movieid = id and rentmode = 'S' and (sysdate - since) > 7";
		ResultSet rs = InputOutput.execQuery(stmt, query);
		
		Vector<String> temp = new Vector<String>();
		while (rs.next()) {
			String mid = rs.getString("movieid");
			while (mid.length() < 21) {
				mid = mid + " ";
			}
			String title = rs.getString("title");
			while (title.length() < 21) {
				title = title + " ";
			}
			String user = rs.getString("username");
			String printRow = mid + title + user;
			temp.add(printRow);
		}
		return temp;
	}
	
	private static void fixOverdue(Connection m_con) throws SQLException {
		// customers credit is to be debited the cost difference between long term and short term rental for each movie
		Statement cStmt = InputOutput.newStatement(m_con);
		String cQuery = "select username, s_rentfee, l_rentfee from Rent, Movie where movieid=mid and rentmode = 'S' and (sysdate - since) > 7";
		ResultSet rs = InputOutput.execQuery(cStmt, cQuery);
		Statement fStmt = InputOutput.newStatement(m_con);
		while (rs.next()) {
			String user = rs.getString("username");
			int sFee = rs.getInt("s_rentfee");
			int lFee = rs.getInt("l_rentfee");
			int debit = lFee - sFee;
			String fQuery = "update customer set credit=credit-"+(debit)+" where username='"+user+"'";
			InputOutput.execUpdate(fStmt, fQuery);
		}
		InputOutput.closeStatement(fStmt);
		
		Statement rStmt = InputOutput.newStatement(m_con);
		String rQuery = "update Rent set rentmode = 'L' where rentmode = 'S' and  (sysdate - since) > 7";
		if (InputOutput.execUpdate(rStmt, rQuery)) {
			System.out.println("Successfully updated overdue short term rentals to long term.");
			InputOutput.threadsleep(3000);
		}
	}
	
	private static void prettyUpdate(Vector<String> overdue) {
		InputOutput.clearscreen();
		System.out.println("******************************");
		System.out.println("*   Update user rent modes   *");
		System.out.println("******************************\n");
		System.out.println("Overdue short term rentals: \n");
		System.out.println("   MOVIE ID            MOVIE TITLE         RENTING CUSTOMER\n");
		InputOutput.vectorPrint(overdue);
		System.out.print("\n1. Update overdue short term rentals to long term rentals\n2. Home\nChoice: ");
	}
	
	
}
