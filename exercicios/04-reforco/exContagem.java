import java.util.Scanner;

public class exContagem{
	public static void main(String[] args){
		Scanner sc =  new Scanner(System.in);

		int numero;
		int contagem = 0;
		
		System.out.println("Introduza um numero positivo para começar a contagem.");
		numero = sc.nextInt();

		while(numero < 1){
			System.out.println("Introduza um numero positivo.");
			numero = sc.nextInt();
		}

		while(contagem < numero){
			contagem++;
			
			if(contagem % 2 == 0){
				System.out.println(contagem);
			}
			
		}
	}
}
