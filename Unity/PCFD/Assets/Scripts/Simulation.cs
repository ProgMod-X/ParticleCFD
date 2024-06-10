using System.Collections.Generic;
using UnityEngine;
using Unity.Mathematics;
using UnityEngine.UIElements;
using System.Threading.Tasks;
using System;

public class Simulation : MonoBehaviour
{
    public Mesh ParticleMesh;
    public Material ParticleMaterial;
    private List<Particle> particles = new List<Particle>();
    private List<Vector2> forces = new List<Vector2>();
    public Vector2 boundsSize;
    public int numOfParticles = 500;

    public float interactionRadius;

    private Vector2 gravity = new Vector2(0, -981f);
    public float nearDistanceRequired = 15f;
    public float repulsionEffect = 10000f;
    public float repulsionDropoff = 3f;
    public float viscosityFactor = 4f;
    public float dampeningFactor = 0.8f;
    private List<KeyValuePair<uint, int>> spatialLookup = new List<KeyValuePair<uint, int>>();
    private List<uint> startIndices = new List<uint>();

    public float radius = 10f;



    static readonly List<int2> offsets2D = new List<int2>
    {
        new int2(-1, -1),
        new int2(0, -1),
        new int2(1, -1),
        new int2(-1, 0),
        new int2(1, 0),
        new int2(-1, 1),
        new int2(0, 1),
        new int2(1, 1)
    };

    static readonly uint hashK1 = 15823;
    static readonly uint hashK2 = 9737333;

    int2 GetCell2D(float2 position, float radius)
    {
        return (int2)math.floor(position / radius);
    }

    uint HashCell2D(int2 cell)
    {
        uint2 cellUint = new uint2((uint)cell.x, (uint)cell.y);
        uint a = cellUint.x * hashK1;
        uint b = cellUint.y * hashK2;
        return (a + b);
    }

    uint KeyFromHash(uint hash, uint tableSize)
    {
        return hash % tableSize;
    }

    void UpdateSpatialLookup(Vector2[] points, float radius)
    {
        Parallel.For(0, points.Length, i =>
        {
            int2 cell = GetCell2D(points[i], radius);
            uint cellKey = KeyFromHash(HashCell2D(cell), (uint)points.Length);
            spatialLookup[i] = new KeyValuePair<uint, int>(cellKey, i);
            startIndices[i] = int.MaxValue;
        });

        spatialLookup.Sort((x, y) => x.Key.CompareTo(y.Key));

        Parallel.For(0, points.Length, i =>
        {
            uint key = spatialLookup[i].Key;
            uint keyPrev = i == 0 ? uint.MaxValue : spatialLookup[i - 1].Key;
            if (key != keyPrev)
            {
                startIndices[(int)key] = (uint)i;
            }
        });
    }

    void ForEachPointWithinRadius(Particle samplePoint)
    {
        int2 centre = GetCell2D(samplePoint.Position, radius);
        float sqrRadius = radius * radius;

        foreach (int2 offset in offsets2D)
        {
            uint key = KeyFromHash(HashCell2D(centre + offset), (uint)spatialLookup.Count);
            int cellStartIndex = (int)startIndices[(int)key];

            for (int i = cellStartIndex; i < spatialLookup.Count; i++)
            {
                if (spatialLookup[i].Key != key)
                {
                    break;
                }

                int particleIndex = spatialLookup[i].Value;
                float sqrDst = (particles[particleIndex].Position - samplePoint.Position).sqrMagnitude;

                if (sqrDst <= sqrRadius)
                {
                    // Do something with the particle
                }
            }
        }
    }

    void Start()
    {
        float startMinX = -boundsSize.x / 2 - 1;
        float startMaxX = boundsSize.x / 2 - 1;
        float startMinY = -boundsSize.y / 2 - 1;
        float startMaxY = boundsSize.y / 2 - 1;
        // Example: Create some particles
        for (int i = 0; i < numOfParticles; i++)
        {
            Vector2 position = new Vector2(UnityEngine.Random.Range(startMinX, startMaxX), UnityEngine.Random.Range(startMinY, startMaxY));
            Vector2 velocity = new Vector2(UnityEngine.Random.Range(-1, 1), UnityEngine.Random.Range(-1, 1));
            Color color = new Color(UnityEngine.Random.value * 255, UnityEngine.Random.value * 255, UnityEngine.Random.value * 255);

            Particle particle = new Particle(position, velocity, color, ParticleMesh, ParticleMaterial);
            particles.Add(particle);

            forces.Add(Vector2.zero);
        }
    }

    Vector2 RepulsionForce(Vector2 diff, float distance)
    {
        float forceMagnitude = repulsionEffect / math.pow(distance * repulsionDropoff, 2);
        return diff.normalized * forceMagnitude;
    }

    Vector2 ViscosityForce(Particle particle, Particle iterParticle, float distance, float viscosityFactor)
    {
        return (iterParticle.Velocity - particle.Velocity) / math.pow(distance / viscosityFactor, 2);
    }

    void CalculateForces()
    {
        for (int i = 0; i < numOfParticles; i++)
        {
            forces[i] = Vector2.zero;
            forces[i] += gravity;
            for (int j = 0; j < numOfParticles; j++)
            {
                if (i == j) continue;

                Vector2 diff = particles[i].Position - particles[j].Position;
                float distance = diff.magnitude;

                if (distance > nearDistanceRequired || distance == 0)
                {
                    continue;
                }

                forces[i] += RepulsionForce(diff, distance);
                forces[i] += ViscosityForce(particles[i], particles[j], distance, viscosityFactor);
            }

        }

    }

    void Update()
    {
        // float deltaTime = Time.deltaTime;
        float deltaTime = 0.001f;

        CalculateForces();

        for (int i = 0; i < numOfParticles; i++)
        {
            particles[i].Velocity += forces[i] * deltaTime;
            particles[i].Position += particles[i].Velocity * deltaTime;

            if (particles[i].Position.x <= -boundsSize.x / 2)
            {
                particles[i].Velocity.x *= -dampeningFactor;
                particles[i].Position.x = -boundsSize.x / 2; // set position back to boundary
            }
            else if (particles[i].Position.x >= boundsSize.x / 2)
            {
                particles[i].Velocity.x *= -dampeningFactor;
                particles[i].Position.x = boundsSize.x / 2; // set position back to boundary
            }
            if (particles[i].Position.y <= -boundsSize.y / 2)
            {
                particles[i].Velocity.y *= -dampeningFactor;
                particles[i].Position.y = -boundsSize.y / 2; // set position back to boundary
            }
            else if (particles[i].Position.y >= boundsSize.y / 2)
            {
                particles[i].Velocity.y *= -dampeningFactor;
                particles[i].Position.y = boundsSize.y / 2; // set position back to boundary
            }
        }
    }

    void OnRenderObject()
    {
        foreach (Particle particle in particles)
        {
            ParticleMaterial.color = particle.Color;
            ParticleMaterial.SetPass(0);
            Graphics.DrawMeshNow(particle.Mesh, particle.Position, Quaternion.identity);
        }
    }

    void OnDrawGizmos()
    {
        Gizmos.color = new Color(0, 1, 0, 0.4f);
        Gizmos.DrawWireCube(Vector2.zero, boundsSize);

        if (Application.isPlaying)
        {
            Vector2 mousePos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
            bool isPullInteraction = Input.GetMouseButton(0);
            bool isPushInteraction = Input.GetMouseButton(1);
            bool isInteracting = isPullInteraction || isPushInteraction;
            if (isInteracting)
            {
                Gizmos.color = isPullInteraction ? Color.green : Color.red;
                Gizmos.DrawWireSphere(mousePos, interactionRadius);
            }
        }
    }
}
