/*
 * File: Immoblizer
 * Date: 29/01/2021
 * Description: Physics plugin to stop an object moving, e.g. the pole in the scene
 * Author: Stirling McGee (s1840770)
 * Modifications:
 */

#include <ode/ode.h>
#include <plugins/physics.h>

void webots_physics_init() {

  // get body of the robot part
  dBodyID body = dWebotsGetBodyFromDEF("Pole");

  // get the matching world
  dWorldID world = dBodyGetWorld(body);

  // the joint group ID is 0 to allocate the joint normally
  dJointID joint = dJointCreateFixed(world, 0);

  // attach robot part to the static environment: 0
  dJointAttach(joint, body, 0);

  // fix now: remember current position and rotation
  dJointSetFixed(joint);
}

void webots_physics_step() {
  // nothing to do
}

void webots_physics_cleanup() {
  // nothing to do
}