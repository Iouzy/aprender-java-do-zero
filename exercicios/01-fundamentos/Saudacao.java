// Saudacao.java — 8 setembro 2026, 17:37
import java.util.Scanner;

public class Saudacao{
	public static void main(String[] args){
		Scanner sc = new Scanner(System.in);
		
		System.out.println("Qual é o seu nome? ");
                String nome = sc.nextLine();
                System.out.println("Olá " + nome + ", bem-vindo");
				
		System.out.println("Qual é a sua idade? ");

		if (sc.hasNextInt()){
			
			int idade = sc.nextInt();
			

			if (idade < 0){	
				System.out.println("A idade não pode ser negativa.");
			}
			else if (idade >= 120){
                                System.out.println("Já estás no Guiness??");
			}
			else if (idade >= 18){
				System.out.println("Idade confirmada, tens " + idade + " anos e és maior de idade.");
			}
			else{
				System.out.println("Idade confirmada, tens " + idade + " anos e és menor de idade.");
			}
		}
		else {
			System.out.println("Idade inválida.");
		}		
	}
}
