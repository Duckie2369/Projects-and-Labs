package main;

import javax.swing.JFrame;

public class Main {

	public static void main(String[] args) {
		
		JFrame window = new JFrame(); // Create new window
		
		window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // Let the window close when press "x" sign
		
		window.setResizable(false); // Window can not be change size
		
		window.setTitle("Blue Boy Adventure"); // Window title
		
		
		GamePanel gamePanel = new GamePanel();
		window.add(gamePanel);
		window.setIconImage(gamePanel.player.down1);
		/* Causes this Window to be sized to fit the preferred size and
		layouts of its subcomponents so we can see it*/
		window.pack();
		
		window.setLocationRelativeTo(null); // Window always appear in the center
		
		window.setVisible(true); // Make the window appear on screen
		
		gamePanel.setupGame();
		gamePanel.startGameThread();
	}

}
