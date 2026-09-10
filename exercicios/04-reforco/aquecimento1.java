// aquecimento1.java — 10 setembro 2026, 18:12
import java.util.Scanner;

public class aquecimento1{
	public static void main(String[] args){
		Scanner sc = new Scanner(System.in);
		
		int idade;
		
		System.out.println("Qual é a sua idade?");
		idade = sc.nextInt();
		
		while(idade < 0){
			System.out.println("A idade não pode ser negativa, reintroduza a idade."); 
			idade = sc.nextInt();
		}
		
		System.out.println("Tens " + idade + " anos.");
	}
}
