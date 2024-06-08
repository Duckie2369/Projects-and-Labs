package main;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontFormatException;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.InputStream;
import java.text.DecimalFormat;

import object.OBJ_Heart;
import object.OBJ_Key;
import object.SuperObject;

public class UI {

	GamePanel gp;
	Graphics2D g2;
	Font RetroGaming, TitleFont, ButtonFont;
	BufferedImage heart_full, heart_half, heart_blank;
	public boolean messageOn = false;
	public String message = "";
	int messageCounter = 0;
	public boolean gameFinished = false;
	public String currentDialogue = "";
	public int commandNum = 0;
	public int titleScreenState = 0; 
	
	public UI(GamePanel gp) {
		this.gp = gp;
		
		try {
			InputStream is = getClass().getResourceAsStream("/font/Retro Gaming.ttf");
			RetroGaming = Font.createFont(Font.TRUETYPE_FONT, is);
			is = getClass().getResourceAsStream("/font/menu.TTF");
			TitleFont = Font.createFont(Font.TRUETYPE_FONT, is);
			is = getClass().getResourceAsStream("/font/button.TTF");
			ButtonFont = Font.createFont(Font.TRUETYPE_FONT, is);
		} catch (FontFormatException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		// CREATE HUD OBJECT
		SuperObject heart = new OBJ_Heart(gp);
		heart_full = heart.image;
		heart_half = heart.image2;
		heart_blank = heart.image3;
	}
	
	public void showMessage(String text) {
		
		message = text;
		messageOn = true;
	}
	
	public void draw(Graphics2D g2) {
		
		this.g2 = g2;
		
		g2.setFont(RetroGaming);
		g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
		g2.setColor(Color.white);
		// TITLE STATE
		if(gp.gameState == gp.titleState) {
			drawTitleScreen();
		}
		// PLAY STATE
		if(gp.gameState == gp.playState) {
			drawPlayerLife();
		}
		
		// PAUSE STATE
		if(gp.gameState == gp.pauseState) {
			drawPlayerLife();
			drawPauseScreen();
		}
		
		// DIALOGUE STATE
		if(gp.gameState == gp.dialogueState) {
			drawPlayerLife();
			drawDialogueScreen();
		}
	}
	
	public void drawPlayerLife() {
		
		int x = gp.tileSize/2;
		int y = gp.tileSize/2;		
		int i = 0;
		
		// DRAW MAX LIFE
		while(i < gp.player.maxLife/2) {
			g2.drawImage(heart_blank, x, y, null);
			i++;
			x += gp.tileSize;
		}
		
		// RESET
		x = gp.tileSize/2;
		y = gp.tileSize/2;		
		i = 0;
		
		// DRAW CURRENT LIFE
		while(i < gp.player.life) {
			g2.drawImage(heart_half, x, y, null);
			i++;
			if(i < gp.player.life) {
				g2.drawImage(heart_full, x, y, null);
			}
			i++;
			x += gp.tileSize;
		}
	}
	
	public void drawTitleScreen() {
		
		if(titleScreenState == 0) {
			// BACKGROUND COLOR
			g2.setColor(new Color(0, 255, 255));
			g2.fillRect(0, 0, gp.screenWidth, gp.screenHeight);
			
			// TITLE NAME
			g2.setFont(TitleFont);
			g2.setFont(g2.getFont().deriveFont(Font.BOLD,40F));
			String text = "BLUE BOY ADVENTURE";
			int x = getXforCenterText(text);;
			int y = gp.tileSize*2;
			
			// SHADOW
			g2.setColor(Color.BLACK);
			g2.drawString(text, x+5, y+5);
			
			// TITLE COLOR 
			g2.setColor(Color.BLUE);
			g2.drawString(text, x, y);
			
			// BLUE BOY IMAGE
			x = gp.screenWidth/2 - gp.tileSize;
			y += gp.tileSize;
			g2.drawImage(gp.player.down1, x, y, gp.tileSize*2, gp.tileSize*2, null);
			
			// MENU
			g2.setFont(ButtonFont);
			g2.setFont(g2.getFont().deriveFont(Font.BOLD,30F));
			
			text = "NEW GAME";
			x = getXforCenterText(text);
			y += gp.tileSize*3;
			g2.setColor(Color.white);
			g2.fillRect(x-gp.originalTileSize-5, y-gp.originalTileSize*2, gp.tileSize*4, gp.tileSize);
			g2.setColor(Color.black);
			g2.setStroke(new BasicStroke(5));
			g2.drawRect(x-gp.originalTileSize-5, y-gp.originalTileSize*2, gp.tileSize*4, gp.tileSize);
			g2.setColor(Color.blue);
			g2.drawString(text, x, y);
			if(commandNum == 0) {
				g2.drawImage(gp.player.cursor, x-gp.tileSize*2, y-gp.tileSize+gp.originalTileSize, gp.tileSize, gp.tileSize, null);
			}
			
			text = "LOAD GAME";
			x = getXforCenterText(text);
			y += gp.tileSize*2;
			g2.setColor(Color.white);
			g2.fillRect(x-gp.originalTileSize+5, y-gp.originalTileSize*2, gp.tileSize*4, gp.tileSize);
			g2.setColor(Color.black);
			g2.setStroke(new BasicStroke(5));
			g2.drawRect(x-gp.originalTileSize+5, y-gp.originalTileSize*2, gp.tileSize*4, gp.tileSize);
			g2.setColor(Color.blue);
			g2.drawString(text, x, y);
			if(commandNum == 1) {
				g2.drawImage(gp.player.cursor, x-gp.tileSize*2, y-gp.tileSize+gp.originalTileSize, gp.tileSize, gp.tileSize, null);
			}
			
			text = "QUIT";
			x = getXforCenterText(text);
			y += gp.tileSize*2;
			g2.setColor(Color.white);
			g2.fillRect(x-gp.originalTileSize-40, y-gp.originalTileSize*2, gp.tileSize*4, gp.tileSize);
			g2.setColor(Color.black);
			g2.setStroke(new BasicStroke(5));
			g2.drawRect(x-gp.originalTileSize-40, y-gp.originalTileSize*2, gp.tileSize*4, gp.tileSize);
			g2.setColor(Color.blue);
			g2.drawString(text, x, y);
			if(commandNum == 2) {
				g2.drawImage(gp.player.cursor, x-gp.tileSize*3, y-gp.tileSize+gp.originalTileSize, gp.tileSize, gp.tileSize, null);
			}
		}
		else if(titleScreenState == 1) {
			
			// CLASS SELECTION SCREEN
			g2.setColor(new Color(0, 255, 255));
			g2.fillRect(0, 0, gp.screenWidth, gp.screenHeight);
			
			g2.setColor(Color.black);
			g2.setFont(ButtonFont);
			g2.setFont(g2.getFont().deriveFont(Font.BOLD,35F));
			
			String text = "select your class";
			int x = getXforCenterText(text);
			int y = gp.tileSize*3;
			g2.drawString(text, x, y);
			
			text = "FIGHTER";
			x = getXforCenterText(text);
			y += gp.tileSize*3;
	
			g2.drawString(text, x, y);
			if(commandNum == 0) {
				g2.drawImage(gp.player.cursor, x-gp.tileSize, y-gp.originalTileSize-5, gp.tileSize/2, gp.tileSize/2, null);
			}
			
			text = "THIEF";
			x = getXforCenterText(text);
			y += gp.tileSize;
			g2.drawString(text, x, y);
			if(commandNum == 1) {
				g2.drawImage(gp.player.cursor, x-gp.tileSize, y-gp.originalTileSize-5, gp.tileSize/2, gp.tileSize/2, null);
			}
			
			text = "SORCERER";
			x = getXforCenterText(text);
			y += gp.tileSize;
			g2.drawString(text, x, y);
			if(commandNum == 2) {
				g2.drawImage(gp.player.cursor, x-gp.tileSize, y-gp.originalTileSize-5, gp.tileSize/2, gp.tileSize/2, null);
			}
			
			text = "back";
			x = getXforCenterText(text);
			y += gp.tileSize*2;
			g2.drawString(text, x, y);
			if(commandNum == 3) {
				g2.drawImage(gp.player.cursor, x-gp.tileSize, y-gp.originalTileSize-5, gp.tileSize/2, gp.tileSize/2, null);
			}
		}
		
	}
	
	public void drawPauseScreen() {
		
		g2.setFont(g2.getFont().deriveFont(Font.BOLD,80F));
		String text = "PAUSE";
		int x = getXforCenterText(text);
		int y = gp.screenHeight/2;
		
		g2.drawString(text, x, y);
	}
	
	public void drawDialogueScreen() {
		
		// WINDOW
		int x = gp.tileSize*2;
		int y = gp.tileSize/2;
		int width = gp.screenWidth - (gp.tileSize*4);
		int height = gp.tileSize*4;
		
		drawSubWindow(x, y, width, height);
		
		g2.setFont(g2.getFont().deriveFont(Font.PLAIN, 22));
		x += 32;
		y += gp.tileSize;
		
		// New line when meets \n
		for(String line : currentDialogue.split("\n")){
			g2.drawString(currentDialogue, x, y);
			y += 32;
		}
		
	}
	
	public void drawSubWindow(int x, int y, int width, int height) {
		
		// 4th input value: adjusting the opacity (độ mờ) of the window
		Color c = new Color(255, 255, 255, 220);
		g2.setColor(c);
		g2.fillRoundRect(x, y, width, height, 35, 35);
		
		c = new Color(0, 0, 0);
		// Defines the width of outlines of graphics which are rendered with a Graphics2D
		g2.setColor(c);
		g2.setStroke(new BasicStroke(5));
		g2.drawRoundRect(x+5, y+5, width-10, height-10, 25, 25);
	}
	
	public int getXforCenterText(String text) {
		int length = (int)g2.getFontMetrics().getStringBounds(text, g2).getWidth();
		int x = gp.screenWidth/2 - length/2;
		return x;
	}
}
