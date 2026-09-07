import java.util.Scanner;

public class somaPares	{
		public static void main(String[] args){
			Scanner sc = new Scanner(System.in);
			
			int numero = 0;
			int contagem = 1;
			int somaPares = 0;
			
			System.out.println("Introduza um número:");
			numero = sc.nextInt();

			while(numero <= 0){
				System.out.println("O número não pode ser negativo, introduza um número positivo.");
				numero = sc.nextInt();
			}
			
			
			while(contagem < numero){
				contagem++; 
				if(contagem % 2 == 0){
					somaPares = contagem + somaPares;
				}
				
			}
			
			System.out.println("A soma de todos os pares até " + numero + " é de " + somaPares + ".");
	}
}

