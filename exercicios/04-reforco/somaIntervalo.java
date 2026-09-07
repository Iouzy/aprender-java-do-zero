import java.util.Scanner;

public class somaIntervalo{
		public static void main(String[] args){
			Scanner sc = new Scanner(System.in);

			int intervaloInicio = 0;
			int intervaloFinal = 0;
			int contagem = 0;
			int somaPares = 0;
			
			System.out.println("Introduza o intervalo de numeros do qual quer a soma: ");
			System.out.println("Introduza o numero do inicio: ");
			intervaloInicio = sc.nextInt();
			System.out.println("Introduza o numero do final: ");
			intervaloFinal = sc.nextInt();
		
			while(intervaloInicio > intervaloFinal){
				System.out.println("O numero inicial não pode ser superior ao numero final.");
				System.out.println("Reintroduza o numero inicial: ");
				intervaloInicio = sc.nextInt();
			}
			
			contagem = intervaloInicio;
			
			while(contagem <= intervaloFinal){
				if(contagem % 2 == 0){
					somaPares = contagem + somaPares;
				}
				contagem++;
			}

			System.out.println("A soma de todos os pares no intervalo de numeros de " + intervaloInicio + " a " + intervaloFinal + " é de: " + somaPares);
		}

	
}
