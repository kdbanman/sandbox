

public class indRecEngine {
	
	public static void main(String[] args)
	{

		if(args.length == 2){
			indexed.start(io.init(args[0]),args[1]); // INDEXED SEARCH
		}
		else{
			System.out.println("WARNING, INVALID AMOUNT OF ARGUMENTS\nTRY program_name list-of-songs queries");
		}
	}
}
