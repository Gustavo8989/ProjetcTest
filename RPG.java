import java.util.Random;


abstract class Personagem{
    public String nome;
    public int vida;

    public Personagem(String nome, int vida){
        this.nome = nome;
        this.vida = vida;
    }
    public String nome(){
        return nome;
    }
    public int getVida(){
        return vida;
    }
    public abstract void Atacar(double fisico, double magia, double perfurante, double quiemadura); 
}


public class Main{
    public static void main(String[] args){
        Random gerador = new Random();
        double numeroAtk = gerador.nextInt(20);
    }
}
