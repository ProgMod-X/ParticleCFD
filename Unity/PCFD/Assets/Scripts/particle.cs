using UnityEngine;

public class Particle
{
    public Vector2 Position;
    public Vector2 Velocity;
    public Color Color;
    public Mesh Mesh;
    public Material Material;

    public Particle(Vector2 position, Vector2 velocity, Color color, Mesh mesh, Material material)
    {
        Position = position;
        Velocity = velocity;
        Color = color;
        Mesh = mesh;
        Material = material;
    }

    // public void Update(float deltaTime)
    // {
    //     Position += Velocity * deltaTime;
    //     Debug.Log(boundsSize);
    // }
}
