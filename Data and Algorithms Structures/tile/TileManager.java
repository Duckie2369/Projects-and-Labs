package tile;

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import javax.imageio.ImageIO;

import main.GamePanel;
import main.UtilityTool;

public class TileManager {

	GamePanel gp;
	public Tile[] tile;
	public int mapTileNum[][];
	
	public TileManager(GamePanel gp) {
		this.gp = gp;
		
		tile = new Tile[50];
		mapTileNum = new int[gp.maxWorldCol][gp.maxWorldRow];
		
		getTileImage();
		loadMap("/maps/world_map1.txt");
	}
	
	public void getTileImage() {
			
		setup(10, "road04", false);
		setup(11, "road06", false);
		setup(12, "water02", true);
		setup(13, "water04", true);
		setup(14, "water07", true);
		setup(15, "water09", true);
		setup(16, "water03", true);
		setup(17, "water05", true);
		setup(18, "water06", true);
		setup(19, "water08", true);
		setup(20, "grass01", false);
		setup(21, "road01", false);
		setup(22, "sand", false);
		setup(23, "road08", false);
		setup(24, "wall", true);
		setup(25, "road12", false);
		setup(26, "floor01", false);
		setup(27, "earth", false);
		setup(28, "grass00", false);
		setup(29, "water00", true);
		setup(30, "tree", true);
		setup(31, "road00", false);
		setup(32, "water01", true);
		setup(33, "road09", false);
		setup(34, "road11", false);
		setup(35, "road07", false);
		setup(36, "road02", false);
		setup(37, "road03", false);
		setup(38, "road10", false);
		setup(39, "road05", false);
		setup(40, "water12", true);
		setup(41, "water13", true);
		setup(42, "water11", true);
		setup(43, "water10", true);

	}
	
	public void setup(int index, String imageName, boolean collision) {
		
		UtilityTool uTool = new UtilityTool();
		
		try {
			tile[index] = new Tile();
			tile[index].image = ImageIO.read(getClass().getResourceAsStream("/tiles/" + imageName +".png"));
			tile[index].image = uTool.scaleImage(tile[index].image, gp.tileSize, gp.tileSize);
			tile[index].collision = collision;
			
		}catch(IOException e) {
			e.printStackTrace();
		}
	}
	
	public void loadMap(String filePath) {
		
		try {
			InputStream is = getClass().getResourceAsStream(filePath); // Import text file
			BufferedReader br = new BufferedReader(new InputStreamReader(is)); // Read the context of the text file
			
			int col = 0;
			int row = 0;
			
			while (col<gp.maxWorldCol && row<gp.maxWorldRow) {
				
				String line = br.readLine(); // Read a line of 	
				
				while(col<gp.maxWorldCol) {
					String numbers[] = line.split(" "); // Split the string at a space " "
				
					int num = Integer.parseInt(numbers[col]); // Convert the string to integer
				
					mapTileNum[col][row] = num;
					col++;
				}
				if (col == gp.maxWorldCol) {
					col = 0;
					row++;
				}
			}
			br.close();
			
		}catch(Exception e) {
			
		}
	}
	
	public void draw(Graphics2D g2) {
		
		int worldCol = 0;
		int worldRow = 0;
		
		while(worldCol<gp.maxWorldCol && worldRow<gp.maxWorldRow) {
			
			int tileNum = mapTileNum[worldCol][worldRow];
			
			int worldX = worldCol*gp.tileSize;
			int worldY = worldRow*gp.tileSize;
			int screenX = worldX - gp.player.worldX + gp.player.screenX;
			int screenY = worldY - gp.player.worldY + gp.player.screenY;
			
			if(worldX+gp.tileSize*2>gp.player.worldX-gp.player.screenX && 
			   worldX-gp.tileSize*2<gp.player.worldX+gp.player.screenX && 
			   worldY+gp.tileSize*2>gp.player.worldY-gp.player.screenY && 
			   worldY-gp.tileSize*2<gp.player.worldY+gp.player.screenY) {
				
				g2.drawImage(tile[tileNum].image, screenX, screenY, null);

			}
			worldCol++;
			
			if(worldCol == gp.maxWorldCol) {
				worldCol = 0;
				worldRow++;
			}
		
		}
		
	}
}
