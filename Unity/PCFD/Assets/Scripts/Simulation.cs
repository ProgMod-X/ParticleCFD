using System.Collections.Generic;
using UnityEngine;
using Unity.Mathematics;
using UnityEngine.UIElements;

public class Simulation : MonoBehaviour
{
    public Mesh ParticleMesh;
    public Material ParticleMaterial;
    private List<Particle> particles = new List<Particle>();
    private List<Vector2> forces = new List<Vector2>();
    public Vector2 boundsSize;
    public int numOfParticles;

    public float interactionRadius;

    private Vector2 gravity = new Vector2(0, -981f);
    public float nearDistanceRequired = 10f;
    public float repulsionEffect = 1f;
    public float repulsionDropoff = 5f;
    public float viscosityFactor = 6f;
    public float dampeningFactor = 0.8f;


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
        return  (iterParticle.Velocity - particle.Velocity) / math.pow(distance / viscosityFactor, 2);
    }

    void CalculateForces()
    {
        for (int i = 0; i < numOfParticles; i++) {
            forces[i] = Vector2.zero;
            // forces[i] += gravity;
            for (int j = 0; j < numOfParticles; j++) {
                if (i == j) continue;

                Vector2 diff = particles[i].Position - particles[j].Position;
                float distance = diff.magnitude;

                if (distance > nearDistanceRequired || distance == 0) {
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
    float deltaTime = 0.0003f;

    CalculateForces();

    for (int i = 0; i < numOfParticles; i++) {
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
