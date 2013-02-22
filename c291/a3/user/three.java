import java.util.Vector;
import java.sql.*;


public class three {

	public static void menu(String username, Connection m_con) throws SQLException{
		Vector<String> all_media = new Vector<String>();
		Vector<String> ids = new Vector<String>();
		String query = "select id, title, price from media";
		Statement stmt = InputOutput.newStatement(m_con);
		ResultSet rs = InputOutput.execQuery(stmt, query);
		while (rs.next()) {
			String id = rs.getString("id").trim();
			ids.add(id);
			while (id.length() < 21) {
				id = id + " ";
			}
			String title = rs.getString("title").trim();
			while (title.length() < 21) {
				title = title + " ";
			}
			String price = rs.getString("price").trim();
			all_media.add(id + title + price);
		}
		InputOutput.closeStatement(stmt);
		int back = 0;
		while(back == 0){
			InputOutput.clearscreen();
			System.out.println("******************");
			System.out.println("* Discover Media *");
			System.out.println("******************\n");
			System.out.println("   ID                  TITLE               PURCHASE PRICE\n");
			InputOutput.vectorPrint(all_media);
			System.out.print("\n1. Purchase\n2. Rent\n3. Home\nChoice: ");
			
			int command = InputOutput.cleanCommand(InputOutput.read());
			switch (command){
				case 1:
					purchase(ids, all_media, username,m_con);
					InputOutput.clearscreen();
					break;
				case 2:
					rent(username,m_con);
					InputOutput.clearscreen();
					break;
				case 3:
					back = 1;
					InputOutput.clearscreen();
					break;
				default:
					InputOutput.invalidcom();
					break;
			}
		}
	}
	private static void purchase(Vector<String> ids, Vector<String> all_media, String username, Connection m_con) throws SQLException{
		
		int answered = 0;
		while(answered == 0){
			InputOutput.clearscreen();
			System.out.println("************");
			System.out.println("* Purchase *");
			System.out.println("************\n");
			System.out.println("   ID                  TITLE               PURCHASE PRICE\n");
			InputOutput.vectorPrint(all_media);
			System.out.print("\nMedia ID to purchase: ");
			String id = InputOutput.read();
			System.out.print("\nVisibility ('A', 'F', or 'N') of purchase: ");
			String vis = InputOutput.read();
			boolean badVis = false;
			if (!(vis.equals("A") || vis.equals("F") || vis.equals("N"))) {
				badVis = true;
			}

			if(!ids.contains(id)){
				InputOutput.vectorPrint(ids);
				System.out.println(vis);
				System.out.println(id);
				InputOutput.invalidcom();
			}
			else if (badVis) {
				System.out.println("Visibility must be 'A', 'F', or 'N'");
			} else
			{
				
				int price = getPrice(id, m_con);
				int credit = getCredit(username, m_con);
				if (credit == 0) {
					answered =1;
				}
				if(credit >= price){
					debitCustomer(price, username, m_con);
					insertPurchase(id, username, vis, m_con);
					System.out.println("Purchase successful!");
					answered = 1;
				} else {
					System.out.println("You do not have enough credits");
				}

				InputOutput.threadsleep(3000);
			}
		}
	}

	private static void rent(String username, Connection m_con) throws SQLException{
		boolean credit = false;
		boolean copies = false;

		Vector<String> all_movies = new Vector<String>();
		Vector<String> ids = new Vector<String>();
		String query = "select id, title, s_rentfee, l_rentfee from movie, media where mid = id";//This shows all movies
		Statement stmt = InputOutput.newStatement(m_con);
		ResultSet rs = InputOutput.execQuery(stmt, query);
		while (rs.next()) {
			String id = rs.getString("id").trim();
			ids.add(id);
			while (id.length() < 21) {
				id = id + " ";
			}
			String title = rs.getString("title").trim();
			while (title.length() < 21) {
				title = title + " ";
			}
			String s_rentfee = rs.getString("s_rentfee").trim();
			while (s_rentfee.length() < 21) {
				s_rentfee = s_rentfee + " ";
			}
			String l_rentfee = rs.getString("l_rentfee").trim();
			
			all_movies.add(id + title + s_rentfee + l_rentfee);
		}
		InputOutput.closeStatement(stmt);
		int answered = 0;
		while(answered == 0){
			InputOutput.clearscreen();
			System.out.println("********");
			System.out.println("* Rent *");
			System.out.println("********\n");
			System.out.println("   ID                  TITLE               SHORT RENTAL FEE    LONG RENTAL FEE\n");
			InputOutput.vectorPrint(all_movies);
			System.out.print("\nMovie id to rent: ");
			String mid = InputOutput.read();
			System.out.println("\nLong term ('L') or short term ('S'): ");
			String length = InputOutput.read();
			if (!(length.toUpperCase().equals("L") || length.toUpperCase().equals("S"))) mid = "-1";
			System.out.println("\nVisibility ('A', 'F', or 'N'): ");
			String vis = InputOutput.read();
			
			boolean badVis = false;
			if (!(vis.toUpperCase().equals("A") || vis.toUpperCase().equals("F") || vis.toUpperCase().equals("N"))) {
				badVis = true;
			}
			boolean badLen = false;
			if (!(length.toUpperCase().equals("L") || length.toUpperCase().equals("S"))) {
				badLen = true;
			}
			if(!ids.contains(mid)){
				InputOutput.invalidcom();
				break;
			} else if (badVis) {
				System.out.println("Visibility must be ('A', 'F', or 'N')");
			} else if (badLen) {
				System.out.println("Term must be long term ('L') or short term ('S')");
			}
			
			int fee = getRentFee(mid, length, m_con);
			int usercredit = getCredit(username, m_con);
			if (usercredit == 0) {
				answered =1;
			}
			credit = usercredit >= fee;
			copies = copyLeft(mid, m_con);
			if(credit && copies){
				debitCustomer(fee, username, m_con);
				insertRental(username, mid, length, vis, m_con);
				System.out.println("Rent successful!");
				InputOutput.threadsleep(3000);
				answered = 1;
			}
			else if(!credit){
				System.out.println("You do not have enough credits");
				InputOutput.threadsleep(3000);
			}

			else if(!copies){
				insertWaiting(username, mid, m_con);
				System.out.println("There are not enough copies.  You are on the Waiting List");
				InputOutput.threadsleep(3000);
			}
			else {
				InputOutput.invalidcom();
			}
		}
	}
	
	private static int getPrice(String id, Connection m_con) throws SQLException {
		String query = "select price from media where id='"+id+"'";
		Statement stmt = InputOutput.newStatement(m_con);
		ResultSet rs = InputOutput.execQuery(stmt, query);
		int price = -1;
		if (rs.next()) {
			price = rs.getInt("price");
		} else {
			System.out.println("Error in retrieving price.  Set to -1");
			InputOutput.threadsleep(3000);
		}
		InputOutput.closeStatement(stmt);
		return price;
	}
	
	private static int getCredit(String username, Connection m_con) throws SQLException {
		String query = "select credit from customer where username='"+username+"'";
		Statement stmt = InputOutput.newStatement(m_con);
		ResultSet rs = InputOutput.execQuery(stmt, query);
		int credit = -1;
		if (rs.next()) {
			credit = rs.getInt("credit");
		} else {
			System.out.println("Error in retrieving credit.  Set to -1");
			InputOutput.threadsleep(3000);
		}
		InputOutput.closeStatement(stmt);
		return credit;
	}
	
	private static void debitCustomer(int price, String username, Connection m_con) {
		String query = "update customer set credit=credit-"+(price)+" where username='"+username+"'";
		Statement stmt = InputOutput.newStatement(m_con);
		InputOutput.execUpdate(stmt, query);
		InputOutput.closeStatement(stmt);
	}
	
	private static void insertPurchase(String id, String username, String vis, Connection m_con) {
		String query = "insert into buy values ('"+username+"','"+id+"',sysdate,'"+vis+"')";
		Statement stmt = InputOutput.newStatement(m_con);
		InputOutput.execUpdate(stmt, query);
		InputOutput.closeStatement(stmt);
	}
	
	private static int getRentFee(String mid, String length, Connection m_con) throws SQLException {
		String query = "select "+length.toLowerCase()+"_rentfee from movie where mid='"+mid+"'";
		Statement stmt = InputOutput.newStatement(m_con);
		ResultSet rs = InputOutput.execQuery(stmt, query);
		int fee = -1;
		if (rs.next()) {
			fee = rs.getInt(length.toLowerCase()+"_rentfee");
		} else {
			System.out.println("Error in retrieving rental fee.  Set to -1");
			InputOutput.threadsleep(3000);
		}
		InputOutput.closeStatement(stmt);
		return fee;
	}
	
	private static boolean copyLeft(String mid, Connection m_con) throws SQLException {
		String query = "select quantity from movie where mid='"+mid+"'";
		Statement stmt = InputOutput.newStatement(m_con);
		ResultSet rs = InputOutput.execQuery(stmt, query);
		boolean temp = false;
		if (rs.next()) {
			temp = rs.getInt("quantity") > 0;
		}
		InputOutput.closeStatement(stmt);
		return temp;
	}
	
	private static void insertRental(String username, String mid, String length, String vis, Connection m_con) throws SQLException {
		String query = "insert into rent values ('"+username+"','"+mid+"',sysdate,'"+length+"','"+vis+"')";
		Statement stmt = InputOutput.newStatement(m_con);
		InputOutput.execUpdate(stmt, query);
		InputOutput.closeStatement(stmt);
	}
	
	private static void insertWaiting(String username, String mid, Connection m_con) throws SQLException {
		String query = "insert into waitinglist values ('"+username+"','"+mid+"',sysdate)";
		Statement stmt = InputOutput.newStatement(m_con);
		InputOutput.execUpdate(stmt, query);
		InputOutput.closeStatement(stmt);
	}
}
