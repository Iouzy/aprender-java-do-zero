import java.util.Scanner;

public class Tabuada{
	public static void main(String[] args){
		Scanner sc = new Scanner(System.in);
		System.out.println("Bem-vindo ao Tabuada, introduza um numero do qual queira saber a respetiva tabuada");
		int n = sc.nextInt();
		
		for(int o = 1; o <= 10; o++){
			System.out.println(n + " * " + o + " = " + (n*o));
		}
	}
}
