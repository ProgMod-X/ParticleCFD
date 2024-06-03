using UnityEngine;

public class Particle
{
    public Vector3 Position;
    public Vector3 Velocity;
    public Color Color;
    public Mesh Mesh;
    public Material Material;

    public Particle(Vector3 position, Vector3 velocity, Color color, Mesh mesh, Material material)
    {
        Position = position;
        Velocity = velocity;
        Color = color;
        Mesh = mesh;
        Material = material;
    }

    public void Update(float deltaTime)
    {
        Position += Velocity * deltaTime;
    }
}
