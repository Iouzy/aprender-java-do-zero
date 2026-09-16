import java.util.Scanner;

public class notaFinal{
	public static void main(String[] args){
		Scanner sc = new Scanner(System.in);
		
		String nota;
		
		boolean valida = false;
	
		do{
			System.out.println("Introduza a nota final: ");
			nota = sc.nextLine();
			nota = nota.toUpperCase();
			
			switch(nota){
				case "A":
					valida = true;
					System.out.println("Excelente!");
					break;
				case "B":
					valida = true;
					System.out.println("Bom!");
					break;
				case "C":
					valida = true;
					System.out.println("Suficiente!");
					break;
				case "D":
					valida = true;
					System.out.println("Insuficiente.");
					break;
				case "F":
					valida = true;
					System.out.println("Muito Insuficiente.");
					break;
				default:
					System.out.println("Nota inválida. Só são aceites as seguintes notas: A, B, C, D, F.");
			 }
			
		}while(!valida);
	}
}
