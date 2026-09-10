// Programa.java — 10 setembro 2026, 02:42
public class Programa{
	public static void main(String[] args){
		Pessoa p = new Pessoa("Leonardo", "M", 25);	

		Pessoa p1 = new Pessoa("Bia", "F", 18);
		
		p.setIdade(30);	
		System.out.println(p.descricao());
		p1.setIdade(-5);
		System.out.println(p1.descricao());
	}
}


