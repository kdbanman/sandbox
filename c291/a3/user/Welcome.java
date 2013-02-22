import java.util.*;
import java.sql.*;

public class Welcome {
	static Connection m_con;
	static String username;
	static String password;

	public static void main(String[] args) {
		try {
		int oracle = 0,logout = 0,exit = 0;
		InputOutput.clearscreen();
		System.out.println("*****************************************************************");
		System.out.println("*        ATTENTION: This program is best ran in terminal        *");
		System.out.println("* It will run in eclipse; however, some visual issues may occur *");
		System.out.println("*****************************************************************");
		System.out.print("1. Continue\n2. Quit\nYour Choice: ");

		
		int intcommand = InputOutput.cleanCommand(InputOutput.read());
		switch(intcommand){
			case 1:
				exit = 0;
				oracle = 0;
				logout = 0;
				break;
			case 2:
				exit = 1;
				oracle = 1;
				logout = 1;
				InputOutput.clearscreen();
				System.out.println("Goodbye!");
				break;
			default:
				InputOutput.invalidcom();
		}

		String oracleusername;
		String oraclepassword;
		String oracleserver = "jdbc:oracle:thin:@gwynne.cs.ualberta.ca:1521:CRS";

		//Login to oracle loop
		while(oracle == 0){
			InputOutput.clearscreen();
			System.out.println("*******************");
			System.out.println("* Login to Oracle *");
			System.out.println("*******************");
			System.out.print("Oracle username: ");
			oracleusername = InputOutput.read();
			System.out.print("Oracle password: ");
			oraclepassword = InputOutput.read();
			InputOutput.clearscreen();
			System.out.println("\n\nAlright, we are logging into Oracle as:\n"+oracleusername);
			System.out.println("\nWe will connect to the following server:\n"+oracleserver);
			System.out.print("\nLoading JDBC drivers...");
			try{
				String  m_driverName = "oracle.jdbc.driver.OracleDriver";
				Class.forName(m_driverName);
			}catch(Exception e){
				System.out.println(e.getMessage());
			}
			System.out.println(" OK!");
			System.out.print("\nLogging you in...      ");
			try{
				m_con = DriverManager.getConnection(oracleserver, oracleusername, oraclepassword);
				System.out.println(" OK!");
				oracle = 1;
				System.out.println("\nStarting SAML Login in 3 seconds");
			} catch(Exception e){
				System.out.println(e.getMessage()+"\nPlease try again! We will return you to login in 3 seconds");
				oracle = 0;
			}
			InputOutput.threadsleep(3000);
		}

		//SAML login loop
		while(exit == 0){
			int login = 0;
			InputOutput.clearscreen();
			while(login == 0){
				logout = 0;
				System.out.println("***********************");
				System.out.println("* Hello! Please Login *");
				System.out.println("***********************");
				System.out.print("Username: ");
				username = InputOutput.read();
				System.out.print("Password: ");
				password = InputOutput.read();

				Vector<String> validuser = InputOutput.userlist(m_con);
				
				if(validuser.contains(username) && password.equals("")){
					System.out.println("in here");
					login = 1;
					InputOutput.clearscreen();
					break;
				}
				
				if (username.equals("exit")) {
					System.out.println("Closing Oracle connection...");
					m_con.close();
					System.out.println("Oracle connection closed.");
					System.exit(0);
				}

				if(login == 0)
				{
					System.out.println("WARNING! - The user name and password is not correct!\nPlease try again!");
					InputOutput.threadsleep(3000);
					InputOutput.clearscreen();
				}

			}
			//SAML navigation loop
			while(logout == 0){
				System.out.println("**************************");
				System.out.println("*    Welcome to SAML!    *");
				System.out.println("**************************");
				System.out.println("1. View/Edit personal info\n2. View/Edit friends\n3. Discover media\n4. Owned movies\n5. Logout\n6. Exit");
				System.out.print("Choice: ");
				int command = InputOutput.cleanCommand(InputOutput.read());

				switch (command){
					case 1:
						one.menu(username,m_con);
						InputOutput.clearscreen();
						break;
					case 2:
						two.menu(username,m_con);
						InputOutput.clearscreen();
						break;
					case 3:
						three.menu(username,m_con);
						InputOutput.clearscreen();
						break;
					case 4:
						four.menu(username,m_con);
						InputOutput.clearscreen();
						break;
					case 5:
						logout = 1;
						System.out.println("Logout Successful!");
						InputOutput.threadsleep(3000);
						InputOutput.clearscreen();
						break;
					case 6:
						logout = 1;
						exit = 1;
						try{
							InputOutput.clearscreen();
							System.out.print("\nClosing connection to Oracle...");
							m_con.close();
							System.out.println(" OK!");
							System.out.println("Goodbye!");
						}catch(Exception e){
							System.out.println("We could not close your connection to oracle! Try again later or contact administrator");
							logout = 0;
							exit = 0;
						}

						break;
					default:
						InputOutput.invalidcom();
						break;


				}
			}//Welcome screen ends here
		} 
		} catch (Exception e) {
			System.out.println(e.getMessage());
			try {
				m_con.close();
				System.out.println("Oracle connections closed.");
			}catch(Exception e2){
				System.out.println(e2.getMessage());
				System.out.println("We could not close your connection to oracle! Try again later or contact administrator");
		}//Entire Program
	}//Main end
}
}

