import java.util.*;
import java.sql.*;


public class two {

	public static void menu(String username, Connection m_con) throws SQLException{
		int back = 0;
		while(back == 0){
			InputOutput.clearscreen();
			System.out.println("*********************");
			System.out.println("* View/Edit friends *");
			System.out.println("*********************\n");
			System.out.print("1. View/Remove friends\n2. View/Add suggested friends\n3. Home\nChoice: ");
			int command = InputOutput.cleanCommand(InputOutput.read());
			switch (command){
			case 1:
				removeFriend(username,m_con);
				InputOutput.clearscreen();
				break;
			case 2:
				addSuggestedFriend(username,m_con);
				InputOutput.clearscreen();
				break;
			case 3:
				back = 1;
				break;
			default:
				InputOutput.invalidcom();
				break;
			}
		}
	}
	private static void removeFriend(String username, Connection m_con) throws SQLException{

		int back = 0;
		while(back == 0){
			Vector<String> friends = getFriends(username, m_con);
			InputOutput.clearscreen();
			System.out.println("***********************");
			System.out.println("* View/Remove friends *");
			System.out.println("***********************\n");
			InputOutput.vectorPrint(friends);
			System.out.print("\n1. Remove friend\n2. Back\nChoice: ");
			
			int command = InputOutput.cleanCommand(InputOutput.read());
			
			switch (command){
			case 1:
				removeFriend(username,friends,m_con);
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
	private static void addSuggestedFriend(String username, Connection m_con) throws SQLException{
		
		int back = 0;
		while(back == 0){
			Vector<String> suggested_fd = getFrSugg(username, m_con);
			InputOutput.clearscreen();
			System.out.println("********************");
			System.out.println("* View/Add friends *");
			System.out.println("********************\n");
			System.out.println("   USERNAME\n");
			InputOutput.vectorPrint(suggested_fd);
			System.out.print("\n1. Add friend\n2. Back\nChoice: ");
			
			int command = InputOutput.cleanCommand(InputOutput.read());
			
			switch (command){
			case 1:
				addFriend(username, suggested_fd,m_con);
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
	private static void addFriend(String username, Vector<String> suggested_fd, Connection m_con){
		int back = 0;
		while(back == 0){
			InputOutput.clearscreen();
			System.out.println("**************");
			System.out.println("* Add friend *");
			System.out.println("**************\n");
			System.out.println("   USERNAME\n");
			InputOutput.vectorPrint(suggested_fd);
			System.out.print("\nUsername of friend to add: ");
			
			String friend = InputOutput.read();
			if(!suggested_fd.contains(friend)){
				InputOutput.invalidcom();
			}
			else
			{
				String query = "insert into friend values ('"+username+"','"+friend+"')";
				Statement stmt = InputOutput.newStatement(m_con);
				InputOutput.execUpdate(stmt, query);
				InputOutput.closeStatement(stmt);
				System.out.println("Friend added!");
				InputOutput.threadsleep(3000);
				back = 1;
			}
		}
	}
	
	private static void removeFriend(String username, Vector<String> friends, Connection m_con){
		int back = 0;
		while(back == 0){
			InputOutput.clearscreen();
			System.out.println("*****************");
			System.out.println("* Remove friend *");
			System.out.println("*****************\n");
			System.out.println("   USERNAME\n");
			InputOutput.vectorPrint(friends);
			System.out.print("\nUsername to remove from friends: ");
			
			String friend = InputOutput.read();
			
			if(!friends.contains(friend)){
				InputOutput.invalidcom();
			}
			else
			{
				String query = "delete from friend where user1='"+username+"' and user2='"+friend+"' or user1='"+friend+"' and user2='"+username+"'";
				Statement stmt = InputOutput.newStatement(m_con);
				InputOutput.execUpdate(stmt, query);
				InputOutput.closeStatement(stmt);
				System.out.println("Friend removed!");
				InputOutput.threadsleep(3000);
				back = 1;
			}
			System.out.println("finished sleeping");
		}
	}
	
	private static Vector<String> getFrSugg(String username, Connection m_con) throws SQLException {
		Vector<String> suggested_fd = new Vector<String>();
		String query = "((SELECT F.user2 userf FROM Friend F "+
						"WHERE F.user1 IN  "+
						"((SELECT F.user2 as friend1 FROM Friend F WHERE  F.user1 = '"+username+"') UNION (SELECT F.user1 as friend1 FROM Friend F WHERE  F.user2 = '"+username+"')) "+
						"AND F.user2<>'"+username+"') "+
						"UNION  "+
						"(SELECT F.user1 userf FROM Friend F "+
						"WHERE F.user2 IN  "+
						"((SELECT F.user2 as friend1 FROM Friend F WHERE  F.user1 = '"+username+"') UNION (SELECT F.user1 as friend1 FROM Friend F WHERE  F.user2 = '"+username+"')) "+
						"AND F.user1<>'"+username+"')) "+
						"MINUS "+
						"((SELECT F.user2 as friend1 FROM Friend F WHERE  F.user1 = '"+username+"') UNION (SELECT F.user1 as friend1 FROM Friend F WHERE  F.user2 = '"+username+"'))";
		Statement stmt = InputOutput.newStatement(m_con);
		ResultSet rs = InputOutput.execQuery(stmt, query);
		while (rs.next()) {
			suggested_fd.add(rs.getString("userf").trim());
		}
		InputOutput.closeStatement(stmt);
		return suggested_fd;
	}
	
	private static Vector<String> getFriends(String username, Connection m_con) throws SQLException {
		Vector<String> friends = new Vector<String>();
		String query = "(select user2 username from friend where user1 ='"+username+"') union (select user1 username from friend where user2 = '"+username+"')";
		Statement stmt = InputOutput.newStatement(m_con);
		ResultSet rs = InputOutput.execQuery(stmt, query);
		while (rs.next()) {
			friends.add(rs.getString("username").trim());
		}
		InputOutput.closeStatement(stmt);
		return friends;
	}
}
