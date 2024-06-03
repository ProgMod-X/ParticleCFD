using UnityEngine;
using Unity.Mathematics;

public class Simulation : MonoBehaviour {

    public int numOfParticles = 300;
    public float nearDistanceRequired = 25; // pixels
    public  float particleRadius = 4; // pixels

    public float dampeningEffect = 0.8f;
    public float repulsionEffect = 3E3f; // Higher value means stronger repulsion
    public float repulsionDropoff = 5E-2f; // Higher value means faster dropoff and less repulsion
    public float viscosityEffect = 6f; // Higher value means more viscosity
    public float mouseRepulsionEffect = 1E3;
    public float mouseRepulsionDropoff = 1E-2f;
    public float mouseAttractEffect = 5E4f;
    public float mouseAttractDropoff = 7E-2f;

    public Vector2 gravity = new Vector2(0, -9.81f);¨

    public float gridCellSize = nearDistanceRequired;
    public int gridRows = ceil(Screen.height / gridCellSize);
    public int gridCols = ceil(Screen.width / gridCellSize);

    public dict forces = new dict(); // dunno if this works

    // Use this for initialization
    void Start () {
    
    }
    
    // Update is called once per frame
    void Update () {
    
    }
}
